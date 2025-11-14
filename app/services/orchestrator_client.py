"""
Orchestrator Client Service
Handles communication with Orchestrator droplet
Follows INTEGRATION_GUIDE.md patterns
"""
import httpx
import logging
from datetime import datetime
from app.config import settings
from app.models import ServiceStatus

logger = logging.getLogger(__name__)


class OrchestratorClient:
    """Client for communicating with Orchestrator droplet"""

    def __init__(self):
        self.base_url = settings.orchestrator_url

    async def check_health(self) -> ServiceStatus:
        """Check Orchestrator health status"""
        start_time = datetime.utcnow()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/orchestrator/health")
                elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

                if response.status_code == 200:
                    return ServiceStatus(
                        name="Orchestrator",
                        status="online",
                        response_time_ms=elapsed_ms,
                        last_checked=datetime.utcnow().isoformat(),
                        url=self.base_url
                    )
                else:
                    return ServiceStatus(
                        name="Orchestrator",
                        status="degraded",
                        response_time_ms=elapsed_ms,
                        last_checked=datetime.utcnow().isoformat(),
                        url=self.base_url,
                        error=f"HTTP {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Orchestrator health check failed: {e}")
            return ServiceStatus(
                name="Orchestrator",
                status="offline",
                last_checked=datetime.utcnow().isoformat(),
                url=self.base_url,
                error=str(e)
            )

    async def get_metrics(self) -> dict:
        """Get Orchestrator metrics (if available)"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/orchestrator/metrics")

                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
        except Exception as e:
            logger.warning(f"Failed to fetch Orchestrator metrics: {e}")
            return {}


# Singleton instance
orchestrator_client = OrchestratorClient()
