"""
Dashboard Configuration
Follows FPAI TECH_STACK.md and SECURITY_REQUIREMENTS.md
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Service Identity
    droplet_id: str = "dashboard"
    droplet_name: str = "Dashboard"
    version: str = "1.0.0"
    port: int = 8002

    # External Services
    registry_url: str = "http://198.54.123.234:8000"
    orchestrator_url: str = "http://198.54.123.234:8001"

    # Database
    database_url: Optional[str] = None

    # Service Configuration
    heartbeat_interval: int = 60  # seconds
    status_poll_interval: int = 30  # seconds
    cache_ttl: int = 25  # seconds (slightly less than poll interval)

    # Security
    allowed_origins: list[str] = ["*"]  # Allow all for public site
    rate_limit_per_minute: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
