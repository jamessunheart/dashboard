"""
Registry Client Service
Handles communication with Registry droplet
Follows INTEGRATION_GUIDE.md patterns
"""
import httpx
import logging
from typing import Optional
from datetime import datetime, timedelta
from app.config import settings
from app.models import ServiceStatus, RegistrationPayload

logger = logging.getLogger(__name__)


class RegistryClient:
    """Client for communicating with Registry droplet"""

    def __init__(self):
        self.base_url = settings.registry_url
        self.cache: dict = {}
        self.cache_timestamp: Optional[datetime] = None

    async def check_health(self) -> ServiceStatus:
        """Check Registry health status"""
        start_time = datetime.utcnow()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

                if response.status_code == 200:
                    return ServiceStatus(
                        name="Registry",
                        status="online",
                        response_time_ms=elapsed_ms,
                        last_checked=datetime.utcnow().isoformat(),
                        url=self.base_url
                    )
                else:
                    return ServiceStatus(
                        name="Registry",
                        status="degraded",
                        response_time_ms=elapsed_ms,
                        last_checked=datetime.utcnow().isoformat(),
                        url=self.base_url,
                        error=f"HTTP {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Registry health check failed: {e}")
            return ServiceStatus(
                name="Registry",
                status="offline",
                last_checked=datetime.utcnow().isoformat(),
                url=self.base_url,
                error=str(e)
            )

    async def register(self) -> bool:
        """Register this droplet with Registry"""
        try:
            payload = RegistrationPayload(
                droplet_id=settings.droplet_id,
                name=settings.droplet_name,
                port=settings.port,
                capabilities=["web-interface", "system-visualization", "marketing-site"],
                status="active"
            )

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/droplets/register",
                    json=payload.model_dump()
                )

                if response.status_code in [200, 201]:
                    logger.info(f"Successfully registered with Registry")
                    return True
                else:
                    logger.error(f"Registration failed: HTTP {response.status_code}")
                    return False

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False

    async def send_heartbeat(self) -> bool:
        """Send heartbeat to Registry"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{self.base_url}/droplets/heartbeat",
                    json={"droplet_id": settings.droplet_id, "status": "active"}
                )
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"Heartbeat failed: {e}")
            return False

    async def get_droplets(self) -> list[dict]:
        """Get list of all registered droplets (with caching)"""
        # Check cache
        if self.cache_timestamp and (datetime.utcnow() - self.cache_timestamp).seconds < settings.cache_ttl:
            return self.cache.get("droplets", [])

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/droplets")

                if response.status_code == 200:
                    droplets = response.json()
                    # Update cache
                    self.cache["droplets"] = droplets
                    self.cache_timestamp = datetime.utcnow()
                    return droplets
                else:
                    logger.warning(f"Failed to fetch droplets: HTTP {response.status_code}")
                    return self.cache.get("droplets", [])

        except Exception as e:
            logger.error(f"Error fetching droplets: {e}")
            # Return cached data if available
            return self.cache.get("droplets", [])


# Singleton instance
registry_client = RegistryClient()
