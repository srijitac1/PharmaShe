from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime

class BaseAgent(ABC):
    """
    Base class for all worker agents
    """
    
    def __init__(self, name: str):
        self.name = name
        self.description = ""
    
    @abstractmethod
    async def process_query(self, query: str, db: Session) -> Dict[str, Any]:
        """
        Process a query and return structured results
        """
        pass
    
    def _extract_keywords(self, query: str) -> List[str]:
        """
        Extract relevant keywords from the query
        """
        # Simple keyword extraction - can be enhanced with NLP
        keywords = []
        query_lower = query.lower()
        
        # Common pharmaceutical terms
        pharma_terms = [
            "cancer", "oncology", "breast", "ovarian", "cervical", "endometrial",
            "drug", "therapy", "treatment", "molecule", "compound", "api",
            "formulation", "dosage", "indication", "therapeutic", "clinical"
        ]
        
        for term in pharma_terms:
            if term in query_lower:
                keywords.append(term)
        
        return keywords
    
    def _format_response(self, data: Dict[str, Any], summary: str) -> Dict[str, Any]:
        """
        Format agent response in a consistent structure
        """
        return {
            "agent": self.name,
            "summary": summary,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
    
    def _create_error_response(self, error: str) -> Dict[str, Any]:
        """
        Create standardized error response
        """
        return {
            "agent": self.name,
            "summary": f"Error in {self.name} analysis",
            "data": {},
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "status": "error"
        }
