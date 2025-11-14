"""
Dashboard Data Models
Follows FPAI CODE_STANDARDS.md - Type hints required
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class HealthResponse(BaseModel):
    """UDC-compliant health response"""
    status: Literal["active", "inactive", "error"] = "active"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    message: Optional[str] = None


class CapabilitiesResponse(BaseModel):
    """UDC-compliant capabilities response"""
    provides: list[str] = ["web-interface", "system-visualization", "marketing-site"]
    version: str = "1.0.0"
    endpoints: list[str] = [
        "/health",
        "/capabilities",
        "/state",
        "/dependencies",
        "/message",
        "/api/system/status",
        "/api/droplets"
    ]


class StateResponse(BaseModel):
    """UDC-compliant state response"""
    droplet_id: str
    name: str
    status: Literal["active", "inactive", "error"]
    uptime_seconds: float
    last_heartbeat: str
    connected_services: dict[str, bool]


class DependenciesResponse(BaseModel):
    """UDC-compliant dependencies response"""
    required_services: list[str] = ["registry", "orchestrator"]
    optional_services: list[str] = []
    current_status: dict[str, str]


class MessageRequest(BaseModel):
    """UDC-compliant message format"""
    from_droplet: str
    to_droplet: str = "dashboard"
    message_type: str
    payload: dict
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class MessageResponse(BaseModel):
    """Message processing response"""
    success: bool
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ServiceStatus(BaseModel):
    """Status of an external service"""
    name: str
    status: Literal["online", "degraded", "offline"]
    response_time_ms: Optional[int] = None
    last_checked: str
    url: str
    error: Optional[str] = None


class SystemStatus(BaseModel):
    """Aggregated system status"""
    overall_health: Literal["healthy", "degraded", "critical"]
    services: list[ServiceStatus]
    droplet_count: int
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class DropletInfo(BaseModel):
    """Information about a droplet in the system"""
    droplet_id: str
    name: str
    status: Literal["active", "inactive", "error"]
    port: Optional[int] = None
    description: Optional[str] = None
    capabilities: list[str] = []


class RegistrationPayload(BaseModel):
    """Payload for Registry registration"""
    droplet_id: str
    name: str
    port: int
    capabilities: list[str]
    status: Literal["active", "inactive", "error"] = "active"
