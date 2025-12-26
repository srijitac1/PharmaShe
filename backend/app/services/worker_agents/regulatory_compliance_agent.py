from typing import Dict, Any, List
from sqlalchemy.orm import Session
import json
from .base_agent import BaseAgent

try:
    from app.core.vertex_ai import get_gemini_model
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

class RegulatoryComplianceAgent(BaseAgent):
    """
    Agent specialized in FDA guidelines and regulatory compliance.
    """
    def __init__(self):
        super().__init__("regulatory_compliance")
        self.description = "Checks FDA guidelines and analyzes regulatory compliance requirements"
        self.model = None
        if VERTEX_AI_AVAILABLE:
            try:
                self.model = get_gemini_model()
            except Exception as e:
                print(f"Failed to initialize Vertex AI for RegulatoryComplianceAgent: {e}")

    async def process_query(self, query: str, db: Session) -> Dict[str, Any]:
        """
        Analyzes the query for regulatory compliance using Generative AI.
        """
        if self.model:
            prompt = f"""
            You are a Regulatory Affairs Specialist specialized in FDA guidelines for pharmaceuticals, particularly oncology.
            Analyze the following query regarding regulatory compliance.
            
            Query: "{query}"
            
            Provide a detailed analysis covering:
            1. Relevant FDA Guidelines/Guidances.
            2. Compliance Requirements (IND, NDA, BLA, etc.).
            3. Key Regulatory Risks.
            4. Recommendations for compliance.
            
            Return a JSON object with the following structure:
            {{
                "guidelines": [
                    {{"title": "Guideline Title", "relevance": "High/Medium", "summary": "..."}}
                ],
                "requirements": ["Requirement 1", "Requirement 2"],
                "risks": ["Risk 1", "Risk 2"],
                "recommendations": ["Rec 1", "Rec 2"],
                "summary": "Executive summary of the regulatory stance."
            }}
            """
            try:
                response = self.model.generate_content(prompt)
                text = response.text.strip()
                if "```" in text:
                    text = text.split("```")[1].replace("json", "").strip()
                data = json.loads(text)
                return self._format_response(data, data.get("summary", "Analysis completed."))
            except Exception as e:
                return self._create_error_response(str(e))
        
        return self._create_error_response("Regulatory compliance analysis requires active Vertex AI connection.")