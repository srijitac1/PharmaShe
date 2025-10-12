from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
import json
import asyncio
from datetime import datetime

from app.services.worker_agents.iqvia_agent import IQVIAAgent
from app.services.worker_agents.patent_agent import PatentAgent
from app.services.worker_agents.clinical_trials_agent import ClinicalTrialsAgent
from app.services.worker_agents.exim_agent import EXIMAgent
from app.services.worker_agents.web_intelligence_agent import WebIntelligenceAgent
from app.services.worker_agents.internal_knowledge_agent import InternalKnowledgeAgent
from app.services.worker_agents.report_generator_agent import ReportGeneratorAgent
from app.models.models import ResearchSession, ChatMessage, AgentResult

class MasterAgent:
    """
    Master Agent that orchestrates the conversation and delegates tasks to Worker Agents
    """
    
    def __init__(self):
        self.worker_agents = {
            "iqvia": IQVIAAgent(),
            "patent": PatentAgent(),
            "clinical_trials": ClinicalTrialsAgent(),
            "exim": EXIMAgent(),
            "web_intelligence": WebIntelligenceAgent(),
            "internal_knowledge": InternalKnowledgeAgent(),
            "report_generator": ReportGeneratorAgent()
        }
        
    async def process_query(
        self, 
        query: str, 
        db: Session, 
        background_tasks: BackgroundTasks,
        session_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user query by decomposing it into tasks and delegating to Worker Agents
        """
        try:
            # Analyze the query to determine which agents are needed
            required_agents = await self._analyze_query(query)
            
            # Create or update research session
            if not session_id:
                session = ResearchSession(
                    title=f"Research: {query[:50]}...",
                    query=query,
                    user_id=1  # Default user for now
                )
                db.add(session)
                db.commit()
                db.refresh(session)
                session_id = session.id
            else:
                session = db.query(ResearchSession).filter(ResearchSession.id == session_id).first()
            
            # Save user message
            user_message = ChatMessage(
                session_id=session_id,
                role="user",
                content=query
            )
            db.add(user_message)
            db.commit()
            
            # Execute worker agents in parallel
            agent_results = await self._execute_agents(query, required_agents, db, session_id)
            
            # Synthesize results
            synthesized_response = await self._synthesize_results(query, agent_results)
            
            # Save assistant response
            assistant_message = ChatMessage(
                session_id=session_id,
                role="assistant",
                content=synthesized_response["response"],
                metadata=synthesized_response.get("metadata", {})
            )
            db.add(assistant_message)
            db.commit()
            
            return {
                "response": synthesized_response["response"],
                "session_id": session_id,
                "agent_results": agent_results,
                "metadata": synthesized_response.get("metadata", {})
            }
            
        except Exception as e:
            # Log error and return error response
            error_message = f"I apologize, but I encountered an error while processing your query: {str(e)}"
            
            if session_id:
                error_chat_message = ChatMessage(
                    session_id=session_id,
                    role="assistant",
                    content=error_message,
                    metadata={"error": str(e)}
                )
                db.add(error_chat_message)
                db.commit()
            
            return {
                "response": error_message,
                "session_id": session_id,
                "error": str(e)
            }
    
    async def _analyze_query(self, query: str) -> List[str]:
        """
        Analyze the query to determine which worker agents are needed
        """
        query_lower = query.lower()
        required_agents = []
        
        # Market analysis keywords
        if any(keyword in query_lower for keyword in [
            "market", "sales", "revenue", "growth", "cagr", "competitor", 
            "iqvia", "market size", "commercial"
        ]):
            required_agents.append("iqvia")
        
        # Patent analysis keywords
        if any(keyword in query_lower for keyword in [
            "patent", "ip", "intellectual property", "freedom to operate", 
            "expiry", "expiration", "uspto"
        ]):
            required_agents.append("patent")
        
        # Clinical trials keywords
        if any(keyword in query_lower for keyword in [
            "clinical trial", "phase", "study", "recruiting", "completed",
            "clinicaltrials.gov", "pipeline", "development"
        ]):
            required_agents.append("clinical_trials")
        
        # Trade/EXIM keywords
        if any(keyword in query_lower for keyword in [
            "import", "export", "trade", "api", "formulation", "sourcing",
            "supply chain", "manufacturing"
        ]):
            required_agents.append("exim")
        
        # Web intelligence keywords
        if any(keyword in query_lower for keyword in [
            "latest", "recent", "news", "publication", "research", "guideline",
            "regulatory", "fda", "ema"
        ]):
            required_agents.append("web_intelligence")
        
        # Internal knowledge keywords
        if any(keyword in query_lower for keyword in [
            "internal", "company", "previous", "past", "historical", "strategy"
        ]):
            required_agents.append("internal_knowledge")
        
        # If no specific agents identified, use web intelligence as default
        if not required_agents:
            required_agents = ["web_intelligence"]
        
        return required_agents
    
    async def _execute_agents(
        self, 
        query: str, 
        required_agents: List[str], 
        db: Session, 
        session_id: int
    ) -> Dict[str, Any]:
        """
        Execute the required worker agents in parallel
        """
        tasks = []
        agent_results = {}
        
        for agent_name in required_agents:
            if agent_name in self.worker_agents:
                task = self._execute_single_agent(
                    agent_name, query, db, session_id
                )
                tasks.append((agent_name, task))
        
        # Execute all agents concurrently
        if tasks:
            results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
            
            for i, (agent_name, _) in enumerate(tasks):
                result = results[i]
                if isinstance(result, Exception):
                    agent_results[agent_name] = {
                        "status": "error",
                        "error": str(result),
                        "data": None
                    }
                else:
                    agent_results[agent_name] = result
        
        return agent_results
    
    async def _execute_single_agent(
        self, 
        agent_name: str, 
        query: str, 
        db: Session, 
        session_id: int
    ) -> Dict[str, Any]:
        """
        Execute a single worker agent
        """
        try:
            agent = self.worker_agents[agent_name]
            result = await agent.process_query(query, db)
            
            # Save agent result to database
            agent_result = AgentResult(
                session_id=session_id,
                agent_type=agent_name,
                query=query,
                result_data=result,
                status="completed"
            )
            db.add(agent_result)
            db.commit()
            
            return {
                "status": "completed",
                "data": result,
                "agent": agent_name
            }
            
        except Exception as e:
            # Save error result to database
            agent_result = AgentResult(
                session_id=session_id,
                agent_type=agent_name,
                query=query,
                result_data={},
                status="failed",
                error_message=str(e)
            )
            db.add(agent_result)
            db.commit()
            
            return {
                "status": "error",
                "error": str(e),
                "agent": agent_name
            }
    
    async def _synthesize_results(
        self, 
        query: str, 
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize results from multiple agents into a coherent response
        """
        # Count successful vs failed agents
        successful_agents = [name for name, result in agent_results.items() 
                           if result.get("status") == "completed"]
        failed_agents = [name for name, result in agent_results.items() 
                       if result.get("status") == "error"]
        
        # Build response based on successful agent results
        response_parts = []
        metadata = {
            "agents_used": successful_agents,
            "agents_failed": failed_agents,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add insights from each successful agent
        for agent_name, result in agent_results.items():
            if result.get("status") == "completed":
                agent_data = result.get("data", {})
                if agent_data:
                    response_parts.append(f"**{agent_name.replace('_', ' ').title()} Analysis:**")
                    response_parts.append(agent_data.get("summary", "No summary available"))
                    response_parts.append("")  # Add spacing
        
        # Combine all parts
        if response_parts:
            full_response = "\n".join(response_parts)
        else:
            full_response = "I was unable to gather specific information for your query. Please try rephrasing your question or providing more specific details."
        
        # Add context about failed agents if any
        if failed_agents:
            full_response += f"\n\nNote: Some data sources were temporarily unavailable ({', '.join(failed_agents)})."
        
        return {
            "response": full_response,
            "metadata": metadata
        }
