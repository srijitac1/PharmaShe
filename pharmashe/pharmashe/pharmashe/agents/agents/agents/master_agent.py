from agents.literature_agent import fetch_pubmed
from agents.rrf_agent import reciprocal_rank_fusion

def run_analysis(query: str):
    literature = fetch_pubmed(query)
    ranked = reciprocal_rank_fusion(literature)
    high_confidence = [r for r in ranked if r[1] > 0.01]

    summary = (
        f"This analysis reviewed {len(literature)} biomedical sources. "
        f"High-confidence evidence was prioritized using Reciprocal Rank Fusion, "
        f"inspired by DeepSomatic-style evidence consolidation."
    )

    return {"summary": summary, "evidence": high_confidence}