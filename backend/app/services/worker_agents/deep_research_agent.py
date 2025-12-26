from typing import Dict, Any
from sqlalchemy.orm import Session
from app.services.research_pipeline import build_pipeline
from app.models.schemas import ResearchState
from .base_agent import BaseAgent

class DeepResearchAgent(BaseAgent):
    """
    Deep Research Agent that uses LangGraph for multi-step reasoning
    """
    
    def __init__(self):
        super().__init__("deep_research")
        self.description = "Executes a multi-step deep research pipeline (Genomic -> IP -> Trust Analysis)"
        self.pipeline = build_pipeline()
    
    async def process_query(self, query: str, db: Session) -> Dict[str, Any]:
        """
        Execute the LangGraph pipeline
        """
        try:
            # Simple extraction of focus from query
            # In a real scenario, use an LLM to extract the specific biological entity
            focus = query
            for prefix in ["research on ", "analyze ", "deep research ", "investigate "]:
                if query.lower().startswith(prefix):
                    focus = query[len(prefix):]
                    break
            
            initial_state = ResearchState(
                biological_focus=focus,
                evidence=[],
                rrf_score=0.0,
                logs=[]
            )
            
            # Run the pipeline
            result = await self.pipeline.ainvoke(initial_state)
            
            # Format results
            evidence_data = [
                {"source": e.source, "finding": e.finding, "rank": e.rank}
                for e in result.get("evidence", [])
            ]
            
            data = {
                "biological_focus": result.get("biological_focus"),
                "rrf_score": result.get("rrf_score"),
                "evidence": evidence_data,
                "logs": result.get("logs")
            }
            
            summary = (
                f"Deep research pipeline completed for '{focus}'. "
                f"Calculated Trust Score: {result.get('rrf_score')}. "
                f"Identified {len(evidence_data)} key evidence points."
            )
            
            return self._format_response(data, summary)
            
        except Exception as e:
            return self._create_error_response(str(e))