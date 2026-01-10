# Model Evaluation

## Metrics

- **Validation Loss:** 0.7459  
- **Test Loss:** 0.7459  
- **Validation Perplexity:** 2.11
- **Test Perplexity:** 2.11  
- **BLEU:** 0.401  
- **ROUGE-L:** 0.55 
- **BERTScore F1:** 0.906 

## Explanation of Metrics

- **Loss:** Measures how far the model’s predictions are from the true values. Lower loss indicates better predictions. The close validation and test losses indicate that the model **generalizes well** and is **not overfitting**.  

- **Perplexity:** Measures how well the model predicts the next word in a sequence. Lower values indicate the model is more confident and accurate. Values around 2 are very good, showing the model predicts tokens effectively.  

- **BLEU:** Measures the **exact n-gram overlap** between generated text and reference text. A BLEU of 0.401 indicates **moderate exact matches**, meaning the model sometimes differs in wording but still conveys the intended meaning.  

- **ROUGE-L:** Measures the **longest common subsequence** between generated and reference text. A score of 0.55 suggests the model captures **important sequences and structure** reasonably well.  

- **BERTScore F1:** Evaluates **semantic similarity** using contextual embeddings. A high score of 0.906 shows that the generated text is **very close in meaning** to the reference, even if the exact words differ.  

## Interpretation

The model demonstrates **strong performance in predicting text**, with low validation and test loss as well as low perplexity (~2), indicating it is confident and accurate in predicting the next token. The close alignment between validation and test metrics shows the model generalizes well and is not overfitting. While exact n-gram matches measured by BLEU (0.401) and ROUGE-L (0.55) are moderate, the model reliably captures **key sequences and phrases** from the reference text.

Importantly, the high BERTScore F1 of 0.908 indicates that the generated text is **semantically very close** to the reference, even if the wording differs. This means the model produces outputs that **preserve meaning effectively**, making it suitable for tasks where semantic fidelity matters more than exact word matching. **Note:** Some RoBERTa pooler weights were newly initialized, so additional fine-tuning on a specific downstream task could further improve performance.
