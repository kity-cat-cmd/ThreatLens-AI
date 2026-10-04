"""
Tests for AI analysis functionality
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base, get_db
from app.services.ai_service import AIService
from app.models.threat import ThreatCreate, ThreatType, ThreatSeverity


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a new database session for a test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def ai_service(db_session):
    """Create AI service instance"""
    return AIService(db_session)


class TestAIService:
    """Test cases for AI analysis service"""

    @pytest.mark.asyncio
    async def test_analyze_brute_force_threat(self, ai_service):
        """Test analysis of brute force threat"""
        result = await ai_service.analyze_threat(
            threat_id=1,
            threat_title="Suspicious Login Attempts",
            threat_type="intrusion",
            severity="high",
            source_ip="192.168.1.100",
            description="Multiple failed login attempts detected from IP 192.168.1.100",
            include_recommendations=True
        )

        assert result.threat_id == 1
        assert result.summary is not None
        assert result.technical_analysis is not None
        assert len(result.recommendations) > 0
        assert 1 <= result.severity_score <= 10
        assert 0 <= result.confidence <= 1

    @pytest.mark.asyncio
    async def test_analyze_sql_injection_threat(self, ai_service):
        """Test analysis of SQL injection threat"""
        result = await ai_service.analyze_threat(
            threat_id=2,
            threat_title="Potential SQL Injection",
            threat_type="intrusion",
            severity="critical",
            source_ip="10.0.0.1",
            description="Suspicious SQL commands detected in database queries",
            include_recommendations=True
        )

        assert result.severity_score >= 7  # SQL injection should be high severity
        assert len(result.recommendations) > 0

    @pytest.mark.asyncio
    async def test_analyze_malware_threat(self, ai_service):
        """Test analysis of malware threat"""
        result = await ai_service.analyze_threat(
            threat_id=3,
            threat_title="Malware Detection",
            threat_type="malware",
            severity="critical",
            source_ip=None,
            description="Trojan horse malware detected on the system",
            include_recommendations=True
        )

        assert result.threat_id == 3
        assert "malware" in result.technical_analysis.lower() or "trojan" in result.technical_analysis.lower()
        assert len(result.recommendations) > 0

    @pytest.mark.asyncio
    async def test_analyze_without_recommendations(self, ai_service):
        """Test analysis without recommendations"""
        result = await ai_service.analyze_threat(
            threat_id=4,
            threat_title="Simple Threat",
            threat_type="intrusion",
            severity="low",
            source_ip="192.168.1.1",
            description="Minor security event detected",
            include_recommendations=False
        )

        assert len(result.recommendations) == 0

    def test_generate_recommendations(self, ai_service):
        """Test recommendation generation"""
        recommendations = ai_service._generate_recommendations(
            threat_type="intrusion",
            severity="high",
            analysis="Brute force attack detected"
        )

        assert len(recommendations) > 0
        assert len(recommendations) <= 5  # Max 5 recommendations

    def test_extract_summary(self, ai_service):
        """Test summary extraction"""
        long_analysis = "This is a longer analysis. It contains multiple sentences. This should be truncated if it's too long. " * 10

        summary = ai_service._extract_summary(long_analysis)
        assert len(summary) <= 200
        assert summary.endswith("...") or len(summary) < 200

    def test_generate_cache_key(self, ai_service):
        """Test cache key generation"""
        key1 = ai_service._generate_cache_key("Same description")
        key2 = ai_service._generate_cache_key("Same description")
        key3 = ai_service._generate_cache_key("Different description")

        assert key1 == key2  # Same description should produce same key
        assert key1 != key3  # Different description should produce different key

    def test_caching(self, ai_service):
        """Test that analysis results are cached"""
        import asyncio

        description = "Test caching description"

        # First call should not be cached
        result1 = asyncio.get_event_loop().run_until_complete(
            ai_service.analyze_threat(
                threat_id=1,
                threat_title="Test",
                threat_type="intrusion",
                severity="medium",
                source_ip=None,
                description=description,
                include_recommendations=True
            )
        )

        # Second call with same description should use cache
        result2 = asyncio.get_event_loop().run_until_complete(
            ai_service.analyze_threat(
                threat_id=2,
                threat_title="Test 2",
                threat_type="intrusion",
                severity="medium",
                source_ip=None,
                description=description,
                include_recommendations=True
            )
        )

        # Cached result should have lower confidence
        assert result2.model_used == "cached"
        assert result2.confidence < result1.confidence
