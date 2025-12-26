from typing import Dict, Any
from sqlalchemy.orm import Session
import json

try:
    from app.core.vertex_ai import get_gemini_model
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

class DrugInteractionAgent:
    """
    Agent specialized in identifying drug-drug, drug-food, and drug-condition interactions.
    """
    def __init__(self):
        self.name = "drug_interaction"
        self.model = None
        if VERTEX_AI_AVAILABLE:
            try:
                self.model = get_gemini_model()
            except Exception as e:
                print(f"Failed to initialize Vertex AI for DrugInteractionAgent: {e}")

    async def process_query(self, query: str, db: Session) -> Dict[str, Any]:
        """
        Analyzes the query for drug interactions using Generative AI.
        """
        if self.model:
            prompt = f"""
            You are a clinical pharmacologist specialized in drug interactions. 
            Analyze the following query for potential drug-drug, drug-food, or drug-condition interactions.
            
            Query: "{query}"
            
            Return a JSON object with the following structure:
            {{
                "interactions": [
                    {{"pair": "Drug A + Drug B", "severity": "High/Moderate/Low", "description": "Explanation...", "management": "Recommendation..."}}
                ],
                "summary": "A professional summary of the findings.",
                "disclaimer": "Standard medical disclaimer that this is for informational purposes only."
            }}
            """
            try:
                response = self.model.generate_content(prompt)
                text = response.text.strip()
                # Clean up markdown code blocks if present
                if "```" in text:
                    text = text.split("```")[1].replace("json", "").strip()
                return json.loads(text)
            except Exception as e:
                return {"error": str(e), "summary": "Error analyzing interactions."}
        
        return {
            "summary": "Drug interaction analysis requires active Vertex AI connection.",
            "interactions": []
        }