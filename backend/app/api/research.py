from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import User, ResearchSession, ChatMessage, AgentResult
from app.services.master_agent import MasterAgent

router = APIRouter()
master_agent = MasterAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    session_id: int
    agent_results: dict
    metadata: dict

class SessionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    query: str

class SessionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    query: str
    status: str
    created_at: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint for interacting with the Master Agent
    """
    try:
        result = await master_agent.process_query(
            query=request.message,
            db=db,
            background_tasks=background_tasks,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            agent_results=result.get("agent_results", {}),
            metadata=result.get("metadata", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new research session
    """
    try:
        session = ResearchSession(
            title=session_data.title,
            description=session_data.description,
            query=session_data.query,
            user_id=1  # Default user for now
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return SessionResponse(
            id=session.id,
            title=session.title,
            description=session.description,
            query=session.query,
            status=session.status,
            created_at=session.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[SessionResponse])
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all research sessions
    """
    try:
        sessions = db.query(ResearchSession).offset(skip).limit(limit).all()
        
        return [
            SessionResponse(
                id=session.id,
                title=session.title,
                description=session.description,
                query=session.query,
                status=session.status,
                created_at=session.created_at.isoformat()
            )
            for session in sessions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific research session
    """
    try:
        session = db.query(ResearchSession).filter(ResearchSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionResponse(
            id=session.id,
            title=session.title,
            description=session.description,
            query=session.query,
            status=session.status,
            created_at=session.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all messages for a specific session
    """
    try:
        session = db.query(ResearchSession).filter(ResearchSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
        
        return [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "metadata": message.message_metadata,
                "created_at": message.created_at.isoformat()
            }
            for message in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/agent-results")
async def get_session_agent_results(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all agent results for a specific session
    """
    try:
        session = db.query(ResearchSession).filter(ResearchSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        agent_results = db.query(AgentResult).filter(AgentResult.session_id == session_id).all()
        
        return [
            {
                "id": result.id,
                "agent_type": result.agent_type,
                "query": result.query,
                "result_data": result.result_data,
                "status": result.status,
                "error_message": result.error_message,
                "created_at": result.created_at.isoformat()
            }
            for result in agent_results
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
