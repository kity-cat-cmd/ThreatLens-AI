"""
Analysis API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report import AnalysisRequest, AnalysisResult
from app.services.ai_service import AIService
from app.services.threat_service import ThreatService

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_threat(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze a threat using AI
    """
    # Get threat details
    threat_service = ThreatService(db)
    threat = threat_service.get_threat(request.threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")

    # Perform analysis
    ai_service = AIService(db)
    result = await ai_service.analyze_threat(
        threat_id=threat.id,
        threat_title=threat.title,
        threat_type=threat.type,
        severity=threat.severity,
        source_ip=threat.source_ip,
        description=threat.description,
        include_recommendations=request.include_recommendations,
    )
    return result
