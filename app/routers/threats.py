"""
Threat API routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.threat import Threat, ThreatCreate, ThreatUpdate, ThreatList, ThreatStatistics
from app.services.threat_service import ThreatService

router = APIRouter(prefix="/api/v1/threats", tags=["threats"])


@router.post("", response_model=Threat, status_code=201)
def create_threat(threat_data: ThreatCreate, db: Session = Depends(get_db)):
    """Create a new threat"""
    service = ThreatService(db)
    return service.create_threat(threat_data)


@router.get("/{threat_id}", response_model=Threat)
def get_threat(threat_id: int, db: Session = Depends(get_db)):
    """Get a threat by ID"""
    service = ThreatService(db)
    threat = service.get_threat(threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat


@router.get("", response_model=ThreatList)
def list_threats(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    db: Session = Depends(get_db),
):
    """List all threats with pagination"""
    service = ThreatService(db)
    skip = (page - 1) * page_size
    threats, total = service.list_threats(skip=skip, limit=page_size, status=status, severity=severity)
    return ThreatList(threats=threats, total=total, page=page, page_size=page_size)


@router.patch("/{threat_id}", response_model=Threat)
def update_threat(threat_id: int, threat_data: ThreatUpdate, db: Session = Depends(get_db)):
    """Update a threat"""
    service = ThreatService(db)
    threat = service.update_threat(threat_id, threat_data)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat


@router.delete("/{threat_id}")
def delete_threat(threat_id: int, db: Session = Depends(get_db)):
    """Delete a threat"""
    service = ThreatService(db)
    success = service.delete_threat(threat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Threat not found")
    return {"deleted": True}
