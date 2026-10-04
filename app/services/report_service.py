"""
Report generation service
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.init_db import ReportModel, ThreatModel
from app.models.report import Report, ReportCreate


class ReportService:
    """Service for generating and managing security reports"""

    def __init__(self, db: Session):
        self.db = db

    def create_report(self, report_data: ReportCreate, analysis_text: str = None, recommendations: str = None) -> Report:
        """Create a new security report"""
        db_report = ReportModel(
            threat_id=report_data.threat_id,
            title=report_data.title,
            summary=report_data.summary,
            recommendations=recommendations,
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return self._to_report(db_report)

    def get_report(self, report_id: int) -> Optional[Report]:
        """Get a report by ID"""
        db_report = self.db.query(ReportModel).filter(ReportModel.id == report_id).first()
        if db_report:
            return self._to_report(db_report)
        return None

    def list_reports(self, skip: int = 0, limit: int = 20) -> tuple[List[Report], int]:
        """List reports with pagination"""
        total = self.db.query(ReportModel).count()
        db_reports = self.db.query(ReportModel).order_by(ReportModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_report(r) for r in db_reports], total

    def generate_threat_report(self, threat_id: int, analysis_text: str, recommendations: List[str]) -> Report:
        """Generate a comprehensive threat report"""
        # Get threat details
        threat = self.db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
        if not threat:
            raise ValueError(f"Threat {threat_id} not found")

        # Create report
        report_title = f"Security Report: {threat.title}"
        report_summary = f"Threat analysis for {threat.type} incident with {threat.severity} severity rating."

        db_report = ReportModel(
            threat_id=threat_id,
            title=report_title,
            summary=report_summary,
            recommendations="\n".join(f"- {rec}" for rec in recommendations),
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return self._to_report(db_report)

    def delete_report(self, report_id: int) -> bool:
        """Delete a report"""
        db_report = self.db.query(ReportModel).filter(ReportModel.id == report_id).first()
        if not db_report:
            return False

        self.db.delete(db_report)
        self.db.commit()
        return True

    def _to_report(self, db_report: ReportModel) -> Report:
        """Convert database model to Report model"""
        return Report(
            id=db_report.id,
            threat_id=db_report.threat_id,
            title=db_report.title,
            summary=db_report.summary,
            recommendations=db_report.recommendations,
            severity_score=db_report.severity_score,
            created_at=db_report.created_at,
        )
