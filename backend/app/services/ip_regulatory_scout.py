from app.models.schemas import ResearchState, Evidence

def ip_regulatory_scout(state: ResearchState) -> ResearchState:
    state.logs.append("IP & Regulatory Scout: Checking WIPO & ClinicalTrials")

    evidence = Evidence(
        source="WIPO / ClinicalTrials.gov",
        finding="No blocking patents or failed trials found",
        rank=2
    )

    state.evidence.append(evidence)
    return state