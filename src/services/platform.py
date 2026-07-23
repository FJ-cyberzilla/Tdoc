"""
TDoc Platform Service - Composite diagnostic aggregator.
"""

from src.interfaces import DiagnosticService
from src.services.environment import EnvironmentService
from src.services.health import HealthService


class PlatformService(DiagnosticService):
    """Composite service for platform diagnostics."""

    def __init__(self):
        self.env = EnvironmentService()
        self.health = HealthService()

    def run(self) -> dict:
        """Aggregates environment and health data."""
        return {"environment": self.env.run(), "health": self.health.run()}
