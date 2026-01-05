def reciprocal_rank_fusion(results, k=60):
    scores = {}
    for rank, item in enumerate(results):
        key = item["text"][:50]
        scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked