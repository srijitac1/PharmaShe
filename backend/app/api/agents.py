from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.services.worker_agents.iqvia_agent import IQVIAAgent
from app.services.worker_agents.patent_agent import PatentAgent
from app.services.worker_agents.clinical_trials_agent import ClinicalTrialsAgent
from app.services.worker_agents.exim_agent import EXIMAgent
from app.services.worker_agents.web_intelligence_agent import WebIntelligenceAgent
from app.services.worker_agents.internal_knowledge_agent import InternalKnowledgeAgent
from app.services.worker_agents.report_generator_agent import ReportGeneratorAgent

router = APIRouter()

# Initialize agents
agents = {
    "iqvia": IQVIAAgent(),
    "patent": PatentAgent(),
    "clinical_trials": ClinicalTrialsAgent(),
    "exim": EXIMAgent(),
    "web_intelligence": WebIntelligenceAgent(),
    "internal_knowledge": InternalKnowledgeAgent(),
    "report_generator": ReportGeneratorAgent()
}

@router.get("/")
async def get_agents():
    """
    Get list of available agents
    """
    return {
        "agents": [
            {
                "name": agent_name,
                "description": agent.description,
                "status": "active"
            }
            for agent_name, agent in agents.items()
        ]
    }

@router.get("/{agent_name}")
async def get_agent_info(agent_name: str):
    """
    Get information about a specific agent
    """
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents[agent_name]
    return {
        "name": agent_name,
        "description": agent.description,
        "status": "active",
        "capabilities": [
            "Query processing",
            "Data analysis",
            "Report generation",
            "Real-time updates"
        ]
    }

@router.post("/{agent_name}/query")
async def query_agent(
    agent_name: str,
    query: str,
    db: Session = Depends(get_db)
):
    """
    Query a specific agent
    """
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        agent = agents[agent_name]
        result = await agent.process_query(query, db)
        
        return {
            "agent": agent_name,
            "query": query,
            "result": result,
            "timestamp": result.get("timestamp")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """
    Get status of a specific agent
    """
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent": agent_name,
        "status": "active",
        "last_updated": "2024-01-25T14:30:00Z",
        "health": "healthy",
        "performance": {
            "avg_response_time": "2.5s",
            "success_rate": "98.5%",
            "queries_processed": 1250
        }
    }
