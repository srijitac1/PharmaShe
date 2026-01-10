import os
import glob
import math
import random
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# Settings
# --------------------------
DATA_DIR = "/group/sbms003/sji/datasets/clm_training_final/"
LOCAL_MODEL_PATH = "./gemma3-1b-it-lora-8bit-trainer/checkpoint-59000"
BASE_MODEL_NAME = "google/gemma-3-1b-it"  # from Hugging Face Hub
N_SAMPLES = 100   # the number of validation sample files

device = "cuda" if torch.cuda.is_available() else "cpu"

# --------------------------
# Collect validation files
# --------------------------

# all text files in DATA_DIR and subdirs
files = glob.glob(os.path.join(DATA_DIR, "**/*.txt"), recursive=True)
print(f"Found {len(files)} text files.")

random.seed(42)
random.shuffle(files)
sample_files = random.sample(files, min(N_SAMPLES, len(files)))  
print(f"Using {N_SAMPLES} sample files for evaluation.")

def compute_perplexity(model, tokenizer, files, label, max_length=512):
    losses = []
    model.eval()
    for f in files:
        text = open(f).read()
        enc = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length).to(device)
        with torch.no_grad():
            labels = enc.input_ids.clone()
            outputs = model(**enc, labels=labels)
            losses.append(outputs.loss.item())
    ppl = math.exp(sum(losses) / len(losses))
    print(f"{label} Validation Perplexity: {ppl:.2f}")
    return ppl

# --------------------------
# 1. Local CLM-trained Model
# --------------------------
print("\n[1] Evaluating local CLM-trained checkpoint...")
ft_tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
ft_model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH).to(device)

compute_perplexity(ft_model, ft_tokenizer, sample_files, "CLM-trained")

# --------------------------
# 2. Hugging Face Base Model
# --------------------------
print("\n[2] Evaluating base model from Hugging Face...")
base_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME).to(device)

compute_perplexity(base_model, base_tokenizer, sample_files, "Base")
