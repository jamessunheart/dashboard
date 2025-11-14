"""
Tests for API endpoints
Validates system status and droplet information endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_system_status_endpoint():
    """Test /api/system/status returns aggregated status"""
    response = client.get("/api/system/status")
    assert response.status_code == 200

    data = response.json()
    assert "overall_health" in data
    assert data["overall_health"] in ["healthy", "degraded", "critical"]
    assert "services" in data
    assert isinstance(data["services"], list)
    assert "droplet_count" in data
    assert "last_updated" in data


def test_droplets_endpoint():
    """Test /api/droplets returns list of droplets"""
    response = client.get("/api/droplets")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Check first droplet has required fields
    droplet = data[0]
    assert "droplet_id" in droplet
    assert "name" in droplet
    assert "status" in droplet


def test_home_page():
    """Test home page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Full Potential AI" in response.content


def test_sacred_loop_page():
    """Test Sacred Loop page loads"""
    response = client.get("/sacred-loop")
    assert response.status_code == 200
    assert b"Sacred Loop" in response.content


def test_live_system_page():
    """Test Live System page loads"""
    response = client.get("/live-system")
    assert response.status_code == 200
    assert b"Live System" in response.content


def test_how_it_works_page():
    """Test How It Works page loads"""
    response = client.get("/how-it-works")
    assert response.status_code == 200
    assert b"How It Works" in response.content


def test_get_involved_page():
    """Test Get Involved page loads"""
    response = client.get("/get-involved")
    assert response.status_code == 200
    assert b"Get Involved" in response.content
