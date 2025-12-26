from app.models.schemas import ResearchState, Evidence

def genomic_harvester(state: ResearchState) -> ResearchState:
    state.logs.append("Genomic Harvester: Scanning TCGA-like data")

    evidence = Evidence(
        source="TCGA",
        finding="BRCA1 high-confidence somatic variant identified",
        rank=1
    )

    state.evidence.append(evidence)
    return state