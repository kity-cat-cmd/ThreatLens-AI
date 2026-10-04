"""
Report API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.report import Report, ReportCreate, ReportList
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.post("", response_model=Report, status_code=201)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    """Create a new report"""
    service = ReportService(db)
    return service.create_report(report_data)


@router.get("", response_model=ReportList)
def list_reports(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """List all reports with pagination"""
    service = ReportService(db)
    skip = (page - 1) * page_size
    reports, total = service.list_reports(skip=skip, limit=page_size)
    return ReportList(reports=reports, total=total, page=page, page_size=page_size)


@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a report by ID"""
    service = ReportService(db)
    report = service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete a report"""
    service = ReportService(db)
    success = service.delete_report(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"deleted": True}
