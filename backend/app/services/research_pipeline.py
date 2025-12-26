from langgraph.graph import StateGraph
from app.models.schemas import ResearchState

from app.services.genomic_harvester import genomic_harvester
from app.services.ip_regulatory_scout import ip_regulatory_scout
from app.services.literature_review import literature_review_scout
from app.services.trust_analyst import trust_analyst

def build_pipeline():
    graph = StateGraph(ResearchState)

    graph.add_node("genomic", genomic_harvester)
    graph.add_node("ip", ip_regulatory_scout)
    graph.add_node("literature", literature_review_scout)
    graph.add_node("trust", trust_analyst)

    graph.set_entry_point("genomic")
    graph.add_edge("genomic", "ip")
    graph.add_edge("ip", "literature")
    graph.add_edge("literature", "trust")

    return graph.compile()