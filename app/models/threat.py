"""
Threat data models
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class ThreatSeverity(str, Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(str, Enum):
    """Types of security threats"""
    MALWARE = "malware"
    INTRUSION = "intrusion"
    DATA_BREACH = "data_breach"
    DOS = "dos"
    POLICY_VIOLATION = "policy_violation"
    UNKNOWN = "unknown"


class ThreatStatus(str, Enum):
    """Threat investigation status"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class ThreatBase(BaseModel):
    """Base threat model with common fields"""
    title: str = Field(..., min_length=1, max_length=255, description="Threat title")
    type: ThreatType = Field(..., description="Type of threat")
    severity: ThreatSeverity = Field(..., description="Threat severity level")
    source_ip: Optional[str] = Field(None, description="Source IP address")
    description: str = Field(..., description="Detailed threat description")


class ThreatCreate(ThreatBase):
    """Model for creating a new threat"""
    pass


class ThreatUpdate(BaseModel):
    """Model for updating a threat"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[ThreatType] = None
    severity: Optional[ThreatSeverity] = None
    source_ip: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ThreatStatus] = None


class Threat(ThreatBase):
    """Complete threat model"""
    id: int
    status: ThreatStatus = ThreatStatus.OPEN
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ThreatList(BaseModel):
    """Paginated list of threats"""
    threats: List[Threat]
    total: int
    page: int
    page_size: int


class ThreatStatistics(BaseModel):
    """Threat statistics"""
    total: int
    by_severity: dict
    by_type: dict
    by_status: dict
    recent_count: int  # Last 24 hours
