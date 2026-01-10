# Unsupervised Fine-tuning (Causal Language Modeling, CLM): Failure and Lessons Learned

---

Based on the lightweight generic model **Gemma 3:1B**, we attempted to apply **Causal Language Modeling (CLM)**, also known as **continued pre-training**, which trains the model to predict the next token in a sequence based on preceding tokens. As a result, the model learns the **linguistic patterns and domain-specific knowledge** of a particular field, in addition to its existing general language knowledge. This allows it to better adapt to the target domain and generate more natural and context-appropriate sentences and paragraphs within that domain.

Therefore, we expected the base model to be fine-tuned into a **biomedical-specific LLM**, similar to MedGemma. However, we did **not apply this CLM training for our final model** because the results were not as good as expected. Despite this 'failure' in CLM training, we included this section to discuss potential directions for future improvement.
## 1. Data Prep

To meaningfully improve domain knowledge, hundreds of MB to several GBs of raw text are typically needed. The more data, the better the adaptation. We extracted and sampled such raw text from **DailyMed** or **PubMed** XML data (**8.5GB / 147,866 files**).

| | DailyMed | PubMed |
| :--- | :--- | :--- |
| **Downloaded Data (ZIP, GZ)** | As of 2 Sep, downloaded "HUMAN PRESCRIPTION LABELS" and "HUMAN OTC LABELS" data (21 GB / 133,518 files) | As of 2 Sep, downloaded all files in the "baseline" and "updatefiles" directories from the PubMed Baseline Repository and Daily Update files (59 GB / 1,552 files) |
| **Extracting & Sampling** | From the XML structure, extract the “title” and “text” strings under `component`. | The XML structure contains multiple `PubmedArticle` entries under `PubmedArticleSet`. For each `PubmedArticle`, extract the `ArticleTitle` and `AbstractText` to generate a single TXT file. Select the generated TXT files whose size exceeds 5 KB. |
| **Final Samples (TXT)** | 6.7GB / 133,518 files | 1.8GB / 14,348 files |

## 2. Training Progress

CLM training was conducted on the Kaya server using two V100 GPUs. However, due to the long training time, the process was stopped on the fourth day at **59,000 out of 145,155 steps** (about 41% progress), considering the remaining project schedule. Approximately **60,416,000 tokens** were trained, and during the process, the **loss showed a steady improvement from an initial 2.5256 to around 1.8203**.

## 3. Training Result

It appears that the base model’s optimal parameters may have been **negatively affected by CLM**. Although the trained model demonstrates **better domain-specific knowledge**, it shows **inconsistencies in its responses and between instructions and responses**.

### 3.1. Quantitative Evaluation with Perplexity (PPL)

**Perplexity (PPL)** is a performance metric that indicates how well a language model predicts the next word. It measures the uncertainty in word prediction. The lower the value, the better the model’s performance.

* PPL $\sim$ 1-2: Nearly perfect prediction (almost always choosing the correct token)
* PPL $\sim$ 10: Quite good
* PPL $\sim$ 100 or higher: The model fails to capture the data distribution well

While the base model had a PPL of **21.77**, the CLM-trained model achieved a PPL of **7.60**, showing that it has adapted quite well to the trained domain.

### 3.2. Qualitative Evaluation

The CLM model shows clear learning effects in terms of **professional vocabulary and the style of the documents** it was trained on. However, it **ignores constraints, produces overly lengthy responses** unrelated to the overall context or the question, and also exhibits **hallucinations**. In contrast, the base model is more stable and provides responses aligned with the intended instructions, but it does not demonstrate knowledge specific to the trained domain.

Therefore, we decided to **skip CLM as the initial fine-tuning step**. If response patterns can be improved through instruction-response fine-tuning and domain-specific knowledge can be handled via RAG, it might be better not to apply CLM at all.


**Question**: Describe why oral suspensions are often recommended for pediatric patients instead of tablets. Answer in under 100 words.

| | Base Model | CLM Model |
| :--- | :--- | :--- |
| **Response Summary** | Oral suspensions are frequently preferred for pediatric patients due to their ease of administration, lower risk of choking, and potential for better palatability.  Children often have a natural desire to swallow, and oral suspensions, being easier to ingest, encourage this.  Furthermore, they can be formulated with appealing flavors and colors, boosting compliance. Tablets can pose a choking hazard and require more careful swallowing. | Oral suspensions are frequently used in pediatric patients because of their greater ease of administration and swallowing. Oral suspensions are a smooth, gel-like substance that is not as easily swallowed as tablets, so the patient may swallow a large volume of solution and have a large volume of undissolved powder in the stomach.  This can lead to stomach upset, nausea, vomiting, and diarrhea. <br> Thank you for your time and attention.  We are happy to answer any questions you may have regarding the use of our product.<br>How can I get the best possible dose of our product?  Ask your pharmacist for a dose chart.  How should I store our product?  Store at 20° to 25°C (68° to 77°F) [see USP Controlled Room Temperature].  Discard any used product after 3 months of date.  Keep out of reach of children.  Discard all unused product promptly to avoid contamination.<br>Dispensing instructions<br>Dispense in a tight container.  Store at 20° to 25°C (68° to 77°F) [see USP Controlled Room Temperature].  Discard any used product after 3 months of date.  Keep out of reach of ... |

---

## 4. Future Improvement

The primary objective of CLM is to predict the next token, meaning that it only evaluates how well the model estimates p(token | previous_tokens). However, higher-level qualities, such as accurately following instructions, maintaining logical consistency within responses, and avoiding self-contradictions, cannot be captured by token-level probability alone. Therefore, two potential improvement strategies can be considered:

### 4.1. Dataset Refinement and Reconstruction

We can implement an **instruction-like CLM** by refining and reconstructing the training dataset so that the model is frequently exposed to instruction-response patterns, even in an unsupervised setting.

* **Publicly available QA datasets**: **PubMedQA** and **MedQuAD** can be incorporated to provide examples of domain-specific question-answer pairs that naturally reflect medical reasoning and factual explanation.
* **Instruction-like Data Augmentation**: Automatically extracting segments that contain implicit question-answer or instruction-response structures from DailyMed, PubMed.
* **Curriculum-style Scheduling**: Begin training with ordinary text documents and progressively increase the ratio of instruction-like samples during later training stages, guiding the model to gradually acquire instruction-following behavior.

### 4.2. Best Checkpoint Selection

A lower training loss does not necessarily guarantee better inference performance. Instead of selecting the model checkpoint with the lowest loss, it is more effective to train and evaluate models using direct indicators of instructional consistency, such as:

* **Self-Consistency**: Consistency within the generated response.
* **Instruction–Response Alignment**: Semantic coherence between an instruction and its corresponding response.

By incorporating these metrics when training and selecting the best-performing checkpoint, one can achieve more consistent and instruction-aware results.