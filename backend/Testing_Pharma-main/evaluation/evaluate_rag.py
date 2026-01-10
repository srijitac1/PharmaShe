import os
import re
import math
import torch
from tqdm import tqdm
from rouge import Rouge
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np

# =========================
# CONFIG
# =========================
BASE_MODEL = "google/gemma-3-1b-it"
FINETUNED_MODEL_DIR = "/group/sbms003/common/gemma3-1b-it-excipients-lora/latest"
CHROMA_DIR = "/group/sbms003/common/ChromaDB/"
TEST_FILE = "/group/sbms003/common/data/test.txt"
#TEST_FILE = "/group/sbms003/common/temp/test_3pairs.txt"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# LOAD MODELS
# =========================
print("[INFO] Loading base model...")
base_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
base_model.to(DEVICE).eval()

print("[INFO] Loading fine-tuned model...")
ft_tokenizer = AutoTokenizer.from_pretrained(FINETUNED_MODEL_DIR)
ft_model = AutoModelForCausalLM.from_pretrained(FINETUNED_MODEL_DIR, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
ft_model.to(DEVICE).eval()

# =========================
# LOAD RAG COMPONENTS
# =========================
print("[INFO] Loading ChromaDB vector store...")
embedding_model = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True}
)
retriever = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model).as_retriever(search_kwargs={"k": 3})

# For semantic similarity metric
st_embedder = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1.5",
    trust_remote_code = True
)
rouge = Rouge()
smooth_fn = SmoothingFunction().method1

# =========================
# LOAD TEST DATA
# =========================

def load_prompt_response_pairs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = re.compile(
        r'Prompt:\s*"([^"]+)"\s*Response:\s*"([^"]+)"',
        re.MULTILINE | re.DOTALL
    )
    pairs = pattern.findall(text)
    print(f"[INFO] Loaded {len(pairs)} instruction–response pairs.")
    return pairs

test_data = load_prompt_response_pairs(TEST_FILE)

# =========================
# GENERATION FUNCTIONS
# =========================
def generate(model, tokenizer, prompt, max_new_tokens=128):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text.replace(prompt, "").strip()

def generate_rag(model, tokenizer, query, max_new_tokens=128):
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer concisely:"
    return generate(model, tokenizer, prompt, max_new_tokens=max_new_tokens)

# =========================
# ADDITIONAL METRICS
# =========================
def calculate_precision_recall(generated_tokens, expected_tokens):
    """Token-level precision and recall."""
    gen_set = set(generated_tokens)
    exp_set = set(expected_tokens)
    true_positives = len(gen_set & exp_set)
    precision = true_positives / len(gen_set) if gen_set else 0
    recall = true_positives / len(exp_set) if exp_set else 0
    return precision, recall

def calculate_topk_accuracy(generated, expected, k=3):
    gen_words = generated.split()[:k]
    exp_words = expected.split()
    return 1 if any(word in exp_words for word in gen_words) else 0

 
def calculate_perplexity(model, tokenizer, text):
    encodings = tokenizer(text, return_tensors='pt').to(DEVICE)
    stride = 512
    max_length = model.config.max_position_embeddings if hasattr(model.config, "max_position_embeddings") else 1024
    nlls = []
    for i in range(0, encodings.input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = i + stride
        trg_len = end_loc - i
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100
        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss * trg_len
        nlls.append(neg_log_likelihood)
    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.item()

# =========================
# EVALUATION
# =========================
def evaluate_model(model_name, model, tokenizer, test_data, use_rag=False):
    print(f"\n[INFO] Evaluating {model_name} {'+ RAG' if use_rag else ''}...")
    bleu_scores, rouge_scores, cosine_scores = [], [], []
    precision_scores, recall_scores, topk_scores, ppl_scores = [], [], [], []

    for i, (query, expected) in enumerate(tqdm(test_data, desc=model_name)):
        generated = generate_rag(model, tokenizer, query) if use_rag else generate(model, tokenizer, query)
        if not generated.strip() or not expected.strip():
            bleu, rouge_l, cos_sim, precision, recall, topk, ppl = 0, 0, 0, 0, 0, 0, math.inf
        else:
            bleu = sentence_bleu([expected.split()], generated.split(), smoothing_function=smooth_fn)
            try:
                rouge_l = rouge.get_scores(generated, expected)[0]["rouge-l"]["f"]
            except Exception:
                rouge_l = 0.0
            try:
                emb_expected = st_embedder.encode([expected])
                emb_generated = st_embedder.encode([generated])
                cos_sim = cosine_similarity(emb_expected, emb_generated)[0][0]
            except Exception:
                cos_sim = 0.0
            precision, recall = calculate_precision_recall(generated.split(), expected.split())
            topk = calculate_topk_accuracy(generated, expected, k=3)
            ppl = calculate_perplexity(model, tokenizer, generated)

        bleu_scores.append(bleu)
        rouge_scores.append(rouge_l)
        cosine_scores.append(cos_sim)
        precision_scores.append(precision)
        recall_scores.append(recall)
        topk_scores.append(topk)
        ppl_scores.append(ppl)

        #print(f"✅ {i+1}/{len(test_data)} | BLEU: {bleu:.3f}, ROUGE-L: {rouge_l:.3f}, CosSim: {cos_sim:.3f}, "
        #      f"P: {precision:.3f}, R: {recall:.3f}, TopK: {topk:.1f}, PPL: {ppl:.2f}")

    # Summary
    print(f"\n=== {model_name} {'+ RAG' if use_rag else ''} Evaluation Summary ===")
    print(f"Avg BLEU: {np.mean(bleu_scores):.3f}")
    print(f"Avg ROUGE-L: {np.mean(rouge_scores):.3f}")
    print(f"Avg Cosine Similarity: {np.mean(cosine_scores):.3f}")
    print(f"Avg Precision: {np.mean(precision_scores):.3f}")
    print(f"Avg Recall: {np.mean(recall_scores):.3f}")
    print(f"Top-K Accuracy: {np.mean(topk_scores):.3f}")
    print(f"Avg Perplexity: {np.mean(ppl_scores):.2f}")

    return {
        "BLEU": np.mean(bleu_scores),
        "ROUGE-L": np.mean(rouge_scores),
        "Cosine": np.mean(cosine_scores),
        "Precision": np.mean(precision_scores),
        "Recall": np.mean(recall_scores),
        "TopK": np.mean(topk_scores),
        "Perplexity": np.mean(ppl_scores)
    }

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    results = {}

    results["Base"] = evaluate_model("Gemma Base", base_model, base_tokenizer, test_data, use_rag=False)
    results["Base + RAG"] = evaluate_model("Gemma Base", base_model, base_tokenizer, test_data, use_rag=True)
    results["Fine-tuned"] = evaluate_model("Fine-tuned Model", ft_model, ft_tokenizer, test_data, use_rag=False)
    results["Fine-tuned + RAG"] = evaluate_model("Fine-tuned Model", ft_model, ft_tokenizer, test_data, use_rag=True)

    print("\n=== Final Comparison ===")
    for name, r in results.items():
        print(f"{name:20} | BLEU: {r['BLEU']:.3f} | ROUGE-L: {r['ROUGE-L']:.3f} | CosSim: {r['Cosine']:.3f} | "
              f"P: {r['Precision']:.3f} | R: {r['Recall']:.3f} | TopK: {r['TopK']:.3f} | PPL: {r['Perplexity']:.2f}")
