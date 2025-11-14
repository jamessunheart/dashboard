"""
UDC-Compliant Endpoints
Implements Universal Droplet Contract
Follows UDC_COMPLIANCE.md requirements
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models import (
    HealthResponse,
    CapabilitiesResponse,
    StateResponse,
    DependenciesResponse,
    MessageRequest,
    MessageResponse
)
from app.config import settings
from app.services.registry_client import registry_client
from app.services.orchestrator_client import orchestrator_client
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter()

# Track startup time for uptime calculation
startup_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health():
    """
    UDC-required health endpoint
    Returns current service health status
    """
    return HealthResponse(
        status="active",
        timestamp=datetime.utcnow().isoformat(),
        message="Dashboard is operational"
    )


@router.get("/capabilities", response_model=CapabilitiesResponse)
async def capabilities():
    """
    UDC-required capabilities endpoint
    Returns what this droplet provides
    """
    return CapabilitiesResponse(
        provides=["web-interface", "system-visualization", "marketing-site"],
        version=settings.version,
        endpoints=[
            "/health",
            "/capabilities",
            "/state",
            "/dependencies",
            "/message",
            "/api/system/status",
            "/api/droplets"
        ]
    )


@router.get("/state", response_model=StateResponse)
async def state():
    """
    UDC-required state endpoint
    Returns current droplet state
    """
    # Check connection to services
    registry_status = await registry_client.check_health()
    orchestrator_status = await orchestrator_client.check_health()

    return StateResponse(
        droplet_id=settings.droplet_id,
        name=settings.droplet_name,
        status="active",
        uptime_seconds=time.time() - startup_time,
        last_heartbeat=datetime.utcnow().isoformat(),
        connected_services={
            "registry": registry_status.status == "online",
            "orchestrator": orchestrator_status.status == "online"
        }
    )


@router.get("/dependencies", response_model=DependenciesResponse)
async def dependencies():
    """
    UDC-required dependencies endpoint
    Returns required and optional service dependencies
    """
    # Check current status of dependencies
    registry_status = await registry_client.check_health()
    orchestrator_status = await orchestrator_client.check_health()

    return DependenciesResponse(
        required_services=["registry", "orchestrator"],
        optional_services=[],
        current_status={
            "registry": registry_status.status,
            "orchestrator": orchestrator_status.status
        }
    )


@router.post("/message", response_model=MessageResponse)
async def message(msg: MessageRequest):
    """
    UDC-required message endpoint
    Receives inter-droplet messages
    """
    logger.info(f"Received message from {msg.from_droplet}: {msg.message_type}")

    # Basic message handling (can be extended later)
    if msg.message_type == "ping":
        return MessageResponse(
            success=True,
            message="pong",
            timestamp=datetime.utcnow().isoformat()
        )

    # Log other message types for now
    logger.info(f"Message payload: {msg.payload}")

    return MessageResponse(
        success=True,
        message="Message received",
        timestamp=datetime.utcnow().isoformat()
    )
