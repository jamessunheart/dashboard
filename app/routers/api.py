"""
API Endpoints for Dashboard
Provides system status and droplet information
"""
from fastapi import APIRouter
from app.models import SystemStatus, ServiceStatus, DropletInfo
from app.services.registry_client import registry_client
from app.services.orchestrator_client import orchestrator_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")


@router.get("/system/status", response_model=SystemStatus)
async def get_system_status():
    """
    Get aggregated system status
    Polls Registry and Orchestrator, returns health overview
    """
    # Check all services
    registry_status = await registry_client.check_health()
    orchestrator_status = await orchestrator_client.check_health()

    services = [registry_status, orchestrator_status]

    # Determine overall health
    online_count = sum(1 for s in services if s.status == "online")
    if online_count == len(services):
        overall_health = "healthy"
    elif online_count > 0:
        overall_health = "degraded"
    else:
        overall_health = "critical"

    # Get droplet count from registry
    droplets = await registry_client.get_droplets()
    droplet_count = len(droplets) if droplets else 2  # At minimum Registry + Orchestrator

    return SystemStatus(
        overall_health=overall_health,
        services=services,
        droplet_count=droplet_count,
        last_updated=datetime.utcnow().isoformat()
    )


@router.get("/droplets", response_model=list[DropletInfo])
async def get_droplets():
    """
    Get list of all droplets in the system
    Fetches from Registry with caching
    """
    droplets_data = await registry_client.get_droplets()

    # Transform to DropletInfo format
    droplets = []
    for d in droplets_data:
        droplets.append(DropletInfo(
            droplet_id=d.get("droplet_id", "unknown"),
            name=d.get("name", "Unknown"),
            status=d.get("status", "inactive"),
            port=d.get("port"),
            description=d.get("description"),
            capabilities=d.get("capabilities", [])
        ))

    # If no droplets from registry, return known ones
    if not droplets:
        droplets = [
            DropletInfo(
                droplet_id="registry",
                name="Registry",
                status="active",
                port=8000,
                description="Identity and SSOT management",
                capabilities=["identity", "jwt", "service-directory"]
            ),
            DropletInfo(
                droplet_id="orchestrator",
                name="Orchestrator",
                status="active",
                port=8001,
                description="Task routing and messaging",
                capabilities=["routing", "messaging", "heartbeat-collection"]
            ),
            DropletInfo(
                droplet_id="dashboard",
                name="Dashboard",
                status="active",
                port=8002,
                description="Public marketing site and system visualization",
                capabilities=["web-interface", "system-visualization", "marketing-site"]
            )
        ]

    return droplets


@router.get("/paradise-progress")
async def get_paradise_progress():
    """
    Get paradise progress metrics
    Shows system completion, gaps, and journey to coherence
    """
    # Blueprint: 11 core droplets across 4 phases
    total_droplets = 11

    # Currently built
    built_droplets = 2  # Registry, Orchestrator

    # Calculate progress
    progress_percent = round((built_droplets / total_droplets) * 100)
    gap_count = total_droplets - built_droplets

    # Phase information
    phase_2_total = 3  # Dashboard, Proxy Manager, Verifier
    phase_2_built = 0  # Dashboard in progress
    phase_2_remaining = phase_2_total - phase_2_built

    # Velocity calculation (based on recent progress)
    # We built 2 droplets in ~1 day, so ~1 droplet/day
    velocity = "1 droplet/day"
    days_remaining = gap_count  # At current velocity

    # Estimated completion
    estimated_completion = f"~{days_remaining} days (Phase 4)"

    return {
        "progress_percent": progress_percent,
        "droplets_built": built_droplets,
        "droplets_total": total_droplets,
        "gap_count": gap_count,
        "current_phase": "Phase 2",
        "velocity": velocity,
        "next_milestone": "Dashboard",
        "phase_2_remaining": phase_2_remaining,
        "estimated_completion": estimated_completion,
        "coherence_score": progress_percent,  # Same as progress for now
        "autonomy_level": f"{progress_percent}%"
    }


@router.get("/system-status")
async def get_system_status_simple():
    """
    Simplified system status for paradise-progress page
    """
    # Check services
    registry_status = await registry_client.check_health()
    orchestrator_status = await orchestrator_client.check_health()

    services = [
        {
            "name": "Registry",
            "status": registry_status.status,
            "port": 8000,
            "response_time": registry_status.response_time
        },
        {
            "name": "Orchestrator",
            "status": orchestrator_status.status,
            "port": 8001,
            "response_time": orchestrator_status.response_time
        }
    ]

    return {
        "services": services,
        "total": len(services),
        "online": sum(1 for s in services if s["status"] == "online")
    }
