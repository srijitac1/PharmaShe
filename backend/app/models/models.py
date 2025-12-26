from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    research_sessions = relationship("ResearchSession", back_populates="user")
    reports = relationship("Report", back_populates="user")

class ResearchSession(Base):
    __tablename__ = "research_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    query = Column(Text, nullable=False)
    status = Column(String, default="active")  # active, completed, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="research_sessions")
    messages = relationship("ChatMessage", back_populates="session")
    agent_results = relationship("AgentResult", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON)  # Additional data like agent results, sources, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("ResearchSession", back_populates="messages")

class AgentResult(Base):
    __tablename__ = "agent_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False)
    agent_type = Column(String, nullable=False)  # iqvia, patent, clinical_trials, etc.
    query = Column(Text, nullable=False)
    result_data = Column(JSON, nullable=False)
    status = Column(String, default="completed")  # pending, completed, failed
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("ResearchSession", back_populates="agent_results")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("research_sessions.id"))
    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # pdf, excel, json
    file_path = Column(String)
    report_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")

class Drug(Base):
    __tablename__ = "drugs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    generic_name = Column(String, index=True)
    brand_names = Column(JSON)  # List of brand names
    drug_class = Column(String)
    mechanism_of_action = Column(Text)
    indications = Column(JSON)  # List of approved indications
    dosage_forms = Column(JSON)  # List of available dosage forms
    manufacturer = Column(String)
    patent_expiry = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ClinicalTrial(Base):
    __tablename__ = "clinical_trials"
    
    id = Column(Integer, primary_key=True, index=True)
    nct_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String)  # recruiting, completed, terminated, etc.
    phase = Column(String)
    study_type = Column(String)
    condition = Column(String)
    intervention = Column(String)
    sponsor = Column(String)
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    enrollment = Column(Integer)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Patent(Base):
    __tablename__ = "patents"
    
    id = Column(Integer, primary_key=True, index=True)
    patent_number = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    inventor = Column(String)
    assignee = Column(String)
    filing_date = Column(DateTime)
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    abstract = Column(Text)
    claims = Column(Text)
    drug_name = Column(String, index=True)
    therapeutic_area = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String, index=True)
    therapeutic_area = Column(String, index=True)
    region = Column(String, index=True)
    year = Column(Integer, index=True)
    market_size = Column(Float)  # In USD millions
    growth_rate = Column(Float)  # CAGR percentage
    competitor_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
