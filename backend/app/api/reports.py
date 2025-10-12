from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import Report
import os
import uuid
from datetime import datetime

router = APIRouter()

class ReportRequest(BaseModel):
    title: str
    report_type: str  # pdf, excel, json
    session_id: Optional[int] = None
    template: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    title: str
    report_type: str
    file_path: Optional[str]
    metadata: dict
    created_at: str

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    report_request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new report
    """
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_request.title}_{timestamp}.{report_request.report_type}"
        file_path = f"reports/{filename}"
        
        # Create report record
        report = Report(
            user_id=1,  # Default user for now
            session_id=report_request.session_id,
            title=report_request.title,
            report_type=report_request.report_type,
            file_path=file_path,
            metadata={
                "template": report_request.template,
                "generated_at": datetime.now().isoformat(),
                "status": "generating"
            }
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # TODO: Implement actual report generation logic
        # For now, we'll simulate the process
        
        return ReportResponse(
            id=report.id,
            title=report.title,
            report_type=report.report_type,
            file_path=report.file_path,
            metadata=report.metadata,
            created_at=report.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all reports
    """
    try:
        reports = db.query(Report).offset(skip).limit(limit).all()
        
        return [
            ReportResponse(
                id=report.id,
                title=report.title,
                report_type=report.report_type,
                file_path=report.file_path,
                metadata=report.metadata,
                created_at=report.created_at.isoformat()
            )
            for report in reports
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific report
    """
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return ReportResponse(
            id=report.id,
            title=report.title,
            report_type=report.report_type,
            file_path=report.file_path,
            metadata=report.metadata,
            created_at=report.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{report_id}")
async def download_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Download a report file
    """
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        if not report.file_path or not os.path.exists(report.file_path):
            raise HTTPException(status_code=404, detail="Report file not found")
        
        # TODO: Implement actual file download logic
        # For now, return the file path
        return {"file_path": report.file_path, "download_url": f"/api/reports/download/{report_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document for analysis
    """
    try:
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'txt'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"uploads/{unique_filename}"
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "filename": file.filename,
            "file_path": file_path,
            "file_size": len(content),
            "uploaded_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
