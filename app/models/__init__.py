"""
Data models for ThreatLens AI
"""
from app.models.threat import Threat, ThreatCreate, ThreatUpdate, ThreatSeverity, ThreatType
from app.models.report import Report, ReportCreate

__all__ = [
    "Threat",
    "ThreatCreate",
    "ThreatUpdate",
    "ThreatSeverity",
    "ThreatType",
    "Report",
    "ReportCreate",
]
