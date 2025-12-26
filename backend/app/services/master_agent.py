from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
import json
import asyncio
from datetime import datetime

# Import worker agents
from app.services.worker_agents.iqvia_agent import IQVIAAgent
from app.services.worker_agents.patent_agent import PatentAgent
from app.services.worker_agents.clinical_trials_agent import ClinicalTrialsAgent
from app.services.worker_agents.exim_agent import EXIMAgent
from app.services.worker_agents.web_intelligence_agent import WebIntelligenceAgent
from app.services.worker_agents.internal_knowledge_agent import InternalKnowledgeAgent
from app.services.worker_agents.report_generator_agent import ReportGeneratorAgent
from app.services.worker_agents.drug_interaction_agent import DrugInteractionAgent
from app.services.worker_agents.regulatory_compliance_agent import RegulatoryComplianceAgent
from app.services.worker_agents.deep_research_agent import DeepResearchAgent

# Import models
from app.models.models import ResearchSession, ChatMessage, AgentResult

# Import Vertex AI
try:
    from app.core.vertex_ai import get_gemini_model
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

class MasterAgent:
    """
    Master Agent that orchestrates the research process by delegating to worker agents
    """
    
    def __init__(self):
        self.agents = {
            "iqvia": IQVIAAgent(),
            "patent": PatentAgent(),
            "clinical_trials": ClinicalTrialsAgent(),
            "exim": EXIMAgent(),
            "web_intelligence": WebIntelligenceAgent(),
            "internal_knowledge": InternalKnowledgeAgent(),
            "report_generator": ReportGeneratorAgent(),
            "drug_interaction": DrugInteractionAgent(),
            "regulatory_compliance": RegulatoryComplianceAgent(),
            "deep_research": DeepResearchAgent()
        }
        
        self.model = None
        if VERTEX_AI_AVAILABLE:
            try:
                self.model = get_gemini_model()
            except Exception as e:
                print(f"Failed to initialize Vertex AI: {e}")

    async def process_query(
        self, 
        query: str, 
        db: Session, 
        background_tasks: BackgroundTasks,
        session_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user query by coordinating worker agents
        """
        # 1. Create or retrieve session if needed
        if not session_id:
            session = ResearchSession(
                title=self._generate_title(query),
                query=query,
                user_id=1,  # Default user
                status="active"
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            session_id = session.id
        
        # 2. Save user message
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=query
        )
        db.add(user_msg)
        db.commit()

        # 3. Determine intent and delegate
        selected_agents = await self._route_query(query)
        
        # 4. Execute agents (sequentially to be safe with DB session)
        agent_results = {}
        
        for agent_key in selected_agents:
            if agent_key in self.agents:
                agent = self.agents[agent_key]
                result = await self._execute_agent(agent, query, db, session_id)
                agent_results[agent_key] = result
        
        # 5. Synthesize response
        final_response = await self._synthesize_response(query, agent_results)
        
        # 6. Save assistant message
        asst_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=final_response,
            message_metadata={"agent_results": list(agent_results.keys())}
        )
        db.add(asst_msg)
        db.commit()

        return {
            "response": final_response,
            "session_id": session_id,
            "agent_results": agent_results,
            "metadata": {
                "agents_involved": list(agent_results.keys()),
                "timestamp": datetime.now().isoformat()
            }
        }

    def _generate_title(self, query: str) -> str:
        """Generate a short title from the query"""
        return (query[:47] + "...") if len(query) > 50 else query

    async def _route_query(self, query: str) -> List[str]:
        """
        Determine which agents to use based on the query.
        """
        # Use LLM for routing if available
        if self.model:
            try:
                prompt = f"""
                You are the Master Agent for PharmaShe. Route the following query to the most appropriate worker agents.
                
                Available Agents:
                - iqvia: Market trends, sales data, competitor analysis
                - patent: IP monitoring, patent landscape, freedom-to-operate
                - clinical_trials: Clinical development pipeline, trial status
                - exim: Global trade data, API sourcing, supply chain
                - web_intelligence: Scientific publications, regulatory updates, news
                - internal_knowledge: Internal company documents, past research
                - report_generator: Requests for PDF/Excel reports
                - drug_interaction: Drug-drug, drug-food, or drug-condition interactions and contraindications
                - regulatory_compliance: FDA guidelines, IND/NDA requirements, compliance risks
                - deep_research: Multi-step genomic and IP analysis pipeline for complex biological queries
                
                Query: "{query}"
                
                Return ONLY a JSON list of agent keys (e.g., ["iqvia", "patent"]).
                """
                response = self.model.generate_content(prompt)
                text_response = response.text.strip()
                # Clean up markdown code blocks if present
                if "```" in text_response:
                    text_response = text_response.split("```")[1].replace("json", "").strip()
                
                agents = json.loads(text_response)
                if isinstance(agents, list) and all(isinstance(a, str) for a in agents):
                    # Filter to valid agents
                    valid_agents = [a for a in agents if a in self.agents]
                    if valid_agents:
                        return valid_agents
            except Exception as e:
                print(f"Routing error: {e}")
        
        # Fallback: Keyword matching
        query_lower = query.lower()
        selected = []
        
        if any(w in query_lower for w in ["market", "sales", "revenue", "competitor", "share"]):
            selected.append("iqvia")
        if any(w in query_lower for w in ["patent", "ip", "intellectual property", "expiry", "expiration"]):
            selected.append("patent")
        if any(w in query_lower for w in ["trial", "clinical", "pipeline", "phase", "study"]):
            selected.append("clinical_trials")
        if any(w in query_lower for w in ["trade", "export", "import", "supply", "sourcing", "api"]):
            selected.append("exim")
        if any(w in query_lower for w in ["news", "publication", "article", "journal", "regulatory", "fda", "ema"]):
            selected.append("web_intelligence")
        if any(w in query_lower for w in ["internal", "document", "report", "past project"]):
            selected.append("internal_knowledge")
        if any(w in query_lower for w in ["generate report", "pdf", "excel", "download"]):
            selected.append("report_generator")
        if any(w in query_lower for w in ["interaction", "contraindication", "combine", "safe to take", "side effect"]):
            selected.append("drug_interaction")
        if any(w in query_lower for w in ["fda", "guideline", "compliance", "regulation", "approval", "ind", "nda", "bla"]):
            selected.append("regulatory_compliance")
        if any(w in query_lower for w in ["deep research", "pipeline", "genomic", "rrf", "trust score", "sequence"]):
            selected.append("deep_research")
            
        # Default
        if not selected:
            selected = ["web_intelligence", "internal_knowledge"]
            
        return list(set(selected))

    async def _execute_agent(self, agent, query: str, db: Session, session_id: int) -> Dict[str, Any]:
        """Execute a single agent and save results"""
        try:
            # Execute agent logic
            result = await agent.process_query(query, db)
            
            # Save result to DB
            agent_result_record = AgentResult(
                session_id=session_id,
                agent_type=agent.name,
                query=query,
                result_data=result,
                status="completed"
            )
            db.add(agent_result_record)
            db.commit()
            
            return result
        except Exception as e:
            # Log error
            error_record = AgentResult(
                session_id=session_id,
                agent_type=agent.name,
                query=query,
                result_data={},
                status="failed",
                error_message=str(e)
            )
            db.add(error_record)
            db.commit()
            return {"agent": agent.name, "error": str(e)}

    async def _synthesize_response(self, query: str, agent_results: Dict[str, Any]) -> str:
        """
        Synthesize a final answer from agent results.
        """
        # Use LLM for synthesis if available
        if self.model:
            try:
                # Prepare context (truncate if too large)
                context_data = {k: v.get("data", v) for k, v in agent_results.items()}
                context_str = json.dumps(context_data, default=str)[:30000] # Limit context size
                
                prompt = f"""
                You are the Master Agent for PharmaShe.
                User Query: "{query}"
                
                Synthesize the following agent results into a cohesive, professional response.
                Focus on answering the user's specific question using the data provided.
                
                Agent Results:
                {context_str}
                """
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Synthesis error: {e}")
        
        # Fallback synthesis
        summary_parts = [f"I have analyzed your query '{query}' using the following agents:"]
        
        for agent_name, result in agent_results.items():
            summary_parts.append(f"\n### {agent_name.replace('_', ' ').title()}")
            if "summary" in result:
                summary_parts.append(result["summary"])
            elif "error" in result:
                summary_parts.append(f"Error: {result['error']}")
            else:
                summary_parts.append("Analysis completed.")
        
        return "\n".join(summary_parts)