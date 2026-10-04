"""
Database initialization script
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.database.connection import engine, Base


class ThreatModel(Base):
    """Threat database model"""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    source_ip = Column(String(45), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="open")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')"),
        CheckConstraint("status IN ('open', 'investigating', 'resolved', 'false_positive')"),
    )


class AnalysisModel(Base):
    """Analysis database model"""
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    threat_id = Column(Integer, ForeignKey("threats.id", ondelete="CASCADE"), nullable=False)
    analysis_text = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=True)
    severity_score = Column(Integer, nullable=True)
    confidence = Column(Float, nullable=True)
    model_used = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("severity_score >= 1 AND severity_score <= 10"),
        CheckConstraint("confidence >= 0 AND confidence <= 1"),
    )


class ReportModel(Base):
    """Report database model"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    threat_id = Column(Integer, ForeignKey("threats.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    severity_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


def init_database():
    """Initialize the database by creating all tables"""
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()
