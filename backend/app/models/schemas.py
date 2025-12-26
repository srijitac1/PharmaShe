from typing import List, Dict
from pydantic import BaseModel

class Evidence(BaseModel):
    source: str
    finding: str
    rank: int

class ResearchState(BaseModel):
    biological_focus: str
    evidence: List[Evidence] = []
    rrf_score: float = 0.0
    logs: List[str] = []