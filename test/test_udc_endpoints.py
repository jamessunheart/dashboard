"""
Tests for UDC-compliant endpoints
Ensures Dashboard follows Universal Droplet Contract
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test /health endpoint returns correct format"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] in ["active", "inactive", "error"]
    assert "timestamp" in data


def test_capabilities_endpoint():
    """Test /capabilities endpoint returns correct format"""
    response = client.get("/capabilities")
    assert response.status_code == 200

    data = response.json()
    assert "provides" in data
    assert isinstance(data["provides"], list)
    assert "web-interface" in data["provides"]
    assert "version" in data
    assert "endpoints" in data


def test_state_endpoint():
    """Test /state endpoint returns current droplet state"""
    response = client.get("/state")
    assert response.status_code == 200

    data = response.json()
    assert "droplet_id" in data
    assert data["droplet_id"] == "dashboard"
    assert "name" in data
    assert "status" in data
    assert "uptime_seconds" in data
    assert "connected_services" in data


def test_dependencies_endpoint():
    """Test /dependencies endpoint returns service dependencies"""
    response = client.get("/dependencies")
    assert response.status_code == 200

    data = response.json()
    assert "required_services" in data
    assert "registry" in data["required_services"]
    assert "orchestrator" in data["required_services"]
    assert "current_status" in data


def test_message_endpoint():
    """Test /message endpoint receives messages"""
    message_payload = {
        "from_droplet": "test-droplet",
        "to_droplet": "dashboard",
        "message_type": "ping",
        "payload": {},
        "timestamp": "2025-11-14T00:00:00"
    }

    response = client.post("/message", json=message_payload)
    assert response.status_code == 200

    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "message" in data
