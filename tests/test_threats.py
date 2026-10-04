"""
Tests for threat API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import Base, get_db


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


class TestThreatAPI:
    """Test cases for threat endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "ThreatLens AI" in data["service"]

    def test_create_threat(self):
        """Test creating a new threat"""
        threat_data = {
            "title": "Suspicious Login Attempt",
            "type": "intrusion",
            "severity": "high",
            "source_ip": "192.168.1.100",
            "description": "Multiple failed login attempts from the same IP"
        }
        response = client.post("/api/v1/threats", json=threat_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == threat_data["title"]
        assert data["type"] == threat_data["type"]
        assert data["severity"] == threat_data["severity"]
        assert "id" in data

    def test_get_threat(self):
        """Test getting a specific threat"""
        # Create a threat first
        threat_data = {
            "title": "Test Threat",
            "type": "malware",
            "severity": "critical",
            "description": "Test description"
        }
        create_response = client.post("/api/v1/threats", json=threat_data)
        threat_id = create_response.json()["id"]

        # Get the threat
        response = client.get(f"/api/v1/threats/{threat_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == threat_id
        assert data["title"] == threat_data["title"]

    def test_get_nonexistent_threat(self):
        """Test getting a threat that doesn't exist"""
        response = client.get("/api/v1/threats/9999")
        assert response.status_code == 404

    def test_list_threats(self):
        """Test listing threats"""
        # Create multiple threats
        for i in range(3):
            client.post("/api/v1/threats", json={
                "title": f"Threat {i}",
                "type": "intrusion",
                "severity": "medium",
                "description": f"Description {i}"
            })

        response = client.get("/api/v1/threats?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert "threats" in data
        assert "total" in data
        assert len(data["threats"]) == 3
        assert data["total"] == 3

    def test_list_threats_with_filter(self):
        """Test listing threats with severity filter"""
        # Create threats with different severities
        client.post("/api/v1/threats", json={
            "title": "Critical Threat",
            "type": "malware",
            "severity": "critical",
            "description": "Critical description"
        })
        client.post("/api/v1/threats", json={
            "title": "Low Threat",
            "type": "intrusion",
            "severity": "low",
            "description": "Low description"
        })

        # Filter by critical severity
        response = client.get("/api/v1/threats?severity=critical")
        data = response.json()
        assert data["total"] == 1
        assert data["threats"][0]["severity"] == "critical"

    def test_update_threat(self):
        """Test updating a threat"""
        # Create a threat
        create_response = client.post("/api/v1/threats", json={
            "title": "Original Title",
            "type": "intrusion",
            "severity": "low",
            "description": "Original description"
        })
        threat_id = create_response.json()["id"]

        # Update the threat
        update_data = {
            "title": "Updated Title",
            "severity": "high"
        }
        response = client.patch(f"/api/v1/threats/{threat_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["severity"] == "high"

    def test_delete_threat(self):
        """Test deleting a threat"""
        # Create a threat
        create_response = client.post("/api/v1/threats", json={
            "title": "To Delete",
            "type": "dos",
            "severity": "medium",
            "description": "Will be deleted"
        })
        threat_id = create_response.json()["id"]

        # Delete the threat
        response = client.delete(f"/api/v1/threats/{threat_id}")
        assert response.status_code == 200
        assert response.json()["deleted"] is True

        # Verify it's gone
        get_response = client.get(f"/api/v1/threats/{threat_id}")
        assert get_response.status_code == 404

    def test_get_statistics(self):
        """Test getting threat statistics"""
        # Create some threats
        for i in range(5):
            client.post("/api/v1/threats", json={
                "title": f"Threat {i}",
                "type": "intrusion",
                "severity": "high" if i < 3 else "low",
                "description": f"Description {i}"
            })

        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert "by_severity" in data
        assert "by_type" in data
        assert "by_status" in data
