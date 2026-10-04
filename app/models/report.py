"""
Report data models
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReportBase(BaseModel):
    """Base report model"""
    title: str = Field(..., min_length=1, max_length=255, description="Report title")
    summary: Optional[str] = Field(None, description="Executive summary")


class ReportCreate(ReportBase):
    """Model for creating a report"""
    threat_id: Optional[int] = Field(None, description="Associated threat ID")


class Report(ReportBase):
    """Complete report model"""
    id: int
    threat_id: Optional[int]
    recommendations: Optional[str] = None
    severity_score: Optional[int] = Field(None, ge=1, le=10)
    created_at: datetime

    class Config:
        from_attributes = True


class ReportList(BaseModel):
    """Paginated list of reports"""
    reports: List[Report]
    total: int
    page: int
    page_size: int


class AnalysisRequest(BaseModel):
    """Request for AI analysis"""
    threat_id: int
    include_recommendations: bool = True


class AnalysisResult(BaseModel):
    """AI analysis result"""
    threat_id: int
    summary: str
    technical_analysis: str
    recommendations: List[str]
    severity_score: int = Field(..., ge=1, le=10)
    confidence: float = Field(..., ge=0, le=1)
    model_used: str
