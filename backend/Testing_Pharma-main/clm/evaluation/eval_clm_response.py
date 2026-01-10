import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# Settings
# --------------------------
LOCAL_MODEL_PATH = "./gemma3-1b-it-lora-8bit-trainer/checkpoint-59000"
BASE_MODEL_NAME = "google/gemma-3-1b-it" # from Hugging Face Hub
MAX_NEW_TOKENS = 256
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_model_and_tokenizer(model_path, label):
    print(f"[INFO] Loading {label}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path).to(DEVICE)
    return tokenizer, model

def generate_response(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} \"Your prompt here\"")
        sys.exit(1)

    prompt = sys.argv[1]

    # Load models
    clm_tokenizer, clm_model = load_model_and_tokenizer(LOCAL_MODEL_PATH, "CLM-trained model")
    base_tokenizer, base_model = load_model_and_tokenizer(BASE_MODEL_NAME, "Base model")

    # Generate responses
    print("\n====================")
    print(f"Prompt: {prompt}")
    print("====================\n")

    clm_output = generate_response(clm_model, clm_tokenizer, prompt)
    base_output = generate_response(base_model, base_tokenizer, prompt)

    print("[Local Fine-tuned Model]")
    print(clm_output)
    print("\n[Base Model]")
    print(base_output)

if __name__ == "__main__":
    main()
