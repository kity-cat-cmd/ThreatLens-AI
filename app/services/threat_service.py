"""
Threat management service
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.init_db import ThreatModel, AnalysisModel
from app.models.threat import Threat, ThreatCreate, ThreatUpdate, ThreatStatistics


class ThreatService:
    """Service for managing security threats"""

    def __init__(self, db: Session):
        self.db = db

    def create_threat(self, threat_data: ThreatCreate) -> Threat:
        """Create a new threat"""
        db_threat = ThreatModel(
            title=threat_data.title,
            type=threat_data.type.value,
            severity=threat_data.severity.value,
            source_ip=threat_data.source_ip,
            description=threat_data.description,
            status="open",
        )
        self.db.add(db_threat)
        self.db.commit()
        self.db.refresh(db_threat)
        return self._to_threat(db_threat)

    def get_threat(self, threat_id: int) -> Optional[Threat]:
        """Get a threat by ID"""
        db_threat = self.db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
        if db_threat:
            return self._to_threat(db_threat)
        return None

    def list_threats(
        self, skip: int = 0, limit: int = 20, status: Optional[str] = None, severity: Optional[str] = None
    ) -> tuple[List[Threat], int]:
        """List threats with pagination"""
        query = self.db.query(ThreatModel)

        if status:
            query = query.filter(ThreatModel.status == status)
        if severity:
            query = query.filter(ThreatModel.severity == severity)

        total = query.count()
        db_threats = query.order_by(ThreatModel.created_at.desc()).offset(skip).limit(limit).all()

        return [self._to_threat(t) for t in db_threats], total

    def update_threat(self, threat_id: int, threat_data: ThreatUpdate) -> Optional[Threat]:
        """Update a threat"""
        db_threat = self.db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
        if not db_threat:
            return None

        update_data = threat_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                if hasattr(value, "value"):  # Enum
                    setattr(db_threat, field, value.value)
                else:
                    setattr(db_threat, field, value)

        self.db.commit()
        self.db.refresh(db_threat)
        return self._to_threat(db_threat)

    def delete_threat(self, threat_id: int) -> bool:
        """Delete a threat"""
        db_threat = self.db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
        if not db_threat:
            return False

        self.db.delete(db_threat)
        self.db.commit()
        return True

    def get_statistics(self) -> ThreatStatistics:
        """Get threat statistics"""
        total = self.db.query(ThreatModel).count()

        # Count by severity
        severity_counts = (
            self.db.query(ThreatModel.severity, func.count(ThreatModel.id))
            .group_by(ThreatModel.severity)
            .all()
        )
        by_severity = {s: count for s, count in severity_counts}

        # Count by type
        type_counts = (
            self.db.query(ThreatModel.type, func.count(ThreatModel.id))
            .group_by(ThreatModel.type)
            .all()
        )
        by_type = {t: count for t, count in type_counts}

        # Count by status
        status_counts = (
            self.db.query(ThreatModel.status, func.count(ThreatModel.id))
            .group_by(ThreatModel.status)
            .all()
        )
        by_status = {s: count for s, count in status_counts}

        # Recent threats (last 24 hours)
        yesterday = datetime.now() - timedelta(hours=24)
        recent_count = self.db.query(ThreatModel).filter(ThreatModel.created_at >= yesterday).count()

        return ThreatStatistics(
            total=total,
            by_severity=by_severity,
            by_type=by_type,
            by_status=by_status,
            recent_count=recent_count,
        )

    def _to_threat(self, db_threat: ThreatModel) -> Threat:
        """Convert database model to Threat model"""
        from app.models.threat import ThreatStatus

        return Threat(
            id=db_threat.id,
            title=db_threat.title,
            type=db_threat.type,
            severity=db_threat.severity,
            source_ip=db_threat.source_ip,
            description=db_threat.description,
            status=db_threat.status,
            created_at=db_threat.created_at,
            updated_at=db_threat.updated_at,
        )
