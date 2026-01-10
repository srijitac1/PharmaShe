import os
import glob
from typing import Iterator, List, Dict

from transformers.trainer_utils import get_last_checkpoint
from datetime import timedelta

import torch
from datasets import Dataset, Features, Sequence, Value
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    TrainerCallback,
)
from peft import LoraConfig, get_peft_model
from torch.distributed import is_initialized, get_world_size


# =========================
# Settings
# =========================
HF_TOKEN           = "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"
MODEL_NAME         = "google/gemma-3-1b-it"

DATA_DIR           = "/group/sbms003/sji/datasets/clm_training_final/"
#DATA_GLOB          = "**/f*.txt"
DATA_GLOB          = "**/*.txt"

SEQ_LEN            = 512
OVERLAP_TOKENS     = 64
BATCH_SIZE         = 1
GRAD_ACCUM_STEPS   = 16
LEARNING_RATE      = 2e-5
MAX_TOKENS         = 100_000_000  # Target number of tokens to train (global)
OUTPUT_DIR         = "./gemma3-1b-it-lora-8bit-trainer"

SEED               = 42


# =========================
# Tokenizer
# =========================
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
tokenizer.pad_token = tokenizer.eos_token


# =========================
# Document-level → Sliding chunks (Generator)
#  - Here, only writing to Arrow; shuffling is entirely handled by Trainer's Sampler.
# =========================
def iter_chunks(files: List[str], seq_len: int, overlap: int, add_eos: bool = True) -> Iterator[Dict[str, List[int]]]:
    stride = seq_len - overlap
    pad_id = tokenizer.pad_token_id
    eos_tok = tokenizer.eos_token

    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"[WARN] skip file: {path} ({e})")
            continue

        if add_eos and eos_tok is not None:
            text = text + eos_tok

        ids = tokenizer.encode(text, add_special_tokens=False)
        if not ids:
            continue

        for start in range(0, len(ids), stride):
            chunk = ids[start:start + seq_len]
            if not chunk:
                break
            if len(chunk) < seq_len:
                chunk = chunk + [pad_id] * (seq_len - len(chunk))
            attn = [1 if t != pad_id else 0 for t in chunk]
            yield {"input_ids": chunk, "attention_mask": attn}


def build_dataset() -> Dataset:
    files = sorted(glob.glob(os.path.join(DATA_DIR, DATA_GLOB), recursive=True))
    if len(files) == 0:
        raise FileNotFoundError(f"No files match: {os.path.join(DATA_DIR, DATA_GLOB)}")

    features = Features({
        "input_ids": Sequence(Value("int32")),
        "attention_mask": Sequence(Value("int8")),
    })
    ds = Dataset.from_generator(
        iter_chunks,
        gen_kwargs={"files": files, "seq_len": SEQ_LEN, "overlap": OVERLAP_TOKENS, "add_eos": True},
        features=features
    )
    # Note: ds.shuffle() is NOT called here.
    # Shuffling and non-duplicated consumption are handled by Trainer's Sampler (DistributedSampler in DDP).
    return ds


dataset = build_dataset()


# =========================
# Data Collator
# =========================
collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)


# =========================
# Model (8bit + LoRA) - DDP safe batch
# =========================
bnb_config = BitsAndBytesConfig(load_in_8bit=True)

local_rank_str = os.environ.get("LOCAL_RANK", "0")
try:
    local_rank = int(local_rank_str)
except ValueError:
    local_rank = 0

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA is not available in this process. "
        "Ensure you allocated GPUs via SLURM and run torchrun inside that allocation."
    )

torch.cuda.set_device(local_rank)
device_str = f"cuda:{local_rank}"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN,
    quantization_config=bnb_config,   # 8bit → CUDA required
    device_map={"": device_str},      # Process=GPU 1:1 fixed
    low_cpu_mem_usage=True,
    attn_implementation="eager",      # Recommended for Gemma3
)

lora_cfg = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_cfg)


# =========================
# Token-based stopping callback (global)
#  - Accumulated as (per-device batch × seq_len × world_size)
# =========================
class TokenStoppingCallback(TrainerCallback):
    def __init__(self, max_tokens: int, seq_len: int, per_device_bs: int):
        self.max_tokens = max_tokens
        self.seq_len = seq_len
        self.per_device_bs = per_device_bs
        self.seen = 0

    def on_step_end(self, args, state, control, **kwargs):
        world = get_world_size() if is_initialized() else 1
        tokens_this_step = self.seq_len * self.per_device_bs * world
        self.seen += tokens_this_step
        if self.seen >= self.max_tokens:
            print(f"[INFO] Reached target tokens (global): {self.seen:,}")
            control.should_training_stop = True
        return control


# =========================
# TrainingArguments + Trainer
#   - Sampler handles shuffling/non-duplicated consumption/resume.
#   - dataloader_* tuning to alleviate I/O bottlenecks.
# =========================
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM_STEPS,
    learning_rate=LEARNING_RATE,
    num_train_epochs=3,             # Will stop based on token count
    logging_steps=50,
    save_steps=1000,
    save_total_limit=2,
    fp16=True,                      # V100: fp16
    report_to="none",
    optim="adamw_torch",
    save_safetensors=True,

    # DataLoader tuning
    dataloader_num_workers=4,
    dataloader_pin_memory=True,
    dataloader_persistent_workers=True,
    dataloader_prefetch_factor=2,
    dataloader_drop_last=True,

    # Save Sampler/Scheduler/Optimizer state in the checkpoint
    ddp_find_unused_parameters=True,
    ddp_timeout=600,

    seed=SEED,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset,           # Fixed-length Arrow Dataset
    data_collator=collator,
    processing_class=tokenizer,      # (response to tokenizer deprecated warning)
    callbacks=[TokenStoppingCallback(MAX_TOKENS, SEQ_LEN, BATCH_SIZE)],
)


# =========================
# Training execution (resume supported)
#  - If checkpoint exists, restores Sampler state (shuffle order) → "Continue without duplication"
# =========================
os.makedirs(OUTPUT_DIR, exist_ok=True)
last_ckpt = get_last_checkpoint(OUTPUT_DIR)  # None or checkpoint path
trainer.train(resume_from_checkpoint=last_ckpt)
