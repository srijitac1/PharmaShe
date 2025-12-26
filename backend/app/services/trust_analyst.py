from app.models.schemas import ResearchState

def trust_analyst(state: ResearchState) -> ResearchState:
    state.logs.append("Trust Analyst: Computing Reciprocal Rank Fusion")

    k = 60
    score = sum([1 / (k + e.rank) for e in state.evidence])

    state.rrf_score = round(score, 2)
    return state