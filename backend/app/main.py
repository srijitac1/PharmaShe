from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_db, engine
from app.core.responses import APIResponse
from app.models import models
from app.api import agents, research, reports, auth, external_apis
from app.services.master_agent import MasterAgent

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PharmaShe API",
    description="Women-Centric Cancer Pharmaceutical Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize Master Agent
master_agent = MasterAgent()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(research.router, prefix="/api/research", tags=["Research"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(external_apis.router, prefix="/api/external", tags=["External APIs"])

@app.get("/")
async def root():
    return APIResponse.success({
        "message": "Welcome to PharmaShe API",
        "version": "1.0",
        "docs": "/docs"
    })

@app.get("/health")
async def health_check():
    return APIResponse.success({"status": "healthy", "service": "PharmaShe API"})

@app.post("/api/chat")
async def chat_endpoint(
    message: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Main chat endpoint for interacting with the Master Agent
    """
    try:
        # Process the query through Master Agent
        response = await master_agent.process_query(
            query=message,
            db=db,
            background_tasks=background_tasks
        )
        
        return APIResponse.success(response)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=APIResponse.error(f"An unexpected error occurred: {str(e)}")
        )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
