"""
TDoc Router - Centralized Orchestration Layer.
"""

from typing import Any

from src.exceptions import RouterError
from src.interfaces import DiagnosticService


class TDocRouter:
    """Orchestrates requests between the UI and system modules."""

    def __init__(self, services: dict[str, DiagnosticService]):
        """
        Initializes the router with necessary services.

        Args:
            services: A dictionary containing diagnostic service instances.
        """
        self.services = services

    def route_action(self, action_id: str) -> Any:
        """
        Routes an action request to the appropriate service.
        """
        if action_id == "dashboard":
            return {
                "platform": self.services["platform"].run(),
                "network": self.services["network"].run(),
                "health": self.services["health"].run(),
            }

        service = self.services.get(action_id)

        if not service:
            raise RouterError(f"Unknown action ID: {action_id}")

        try:
            return service.run()
        except Exception as e:
            raise RouterError(f"Error executing action '{action_id}': {e}") from e

    def get_basic_info(self) -> dict[str, Any]:
        """Provides basic system information for the HUD."""
        # For now, return placeholder data.
        return {
            "device": "TDoc System",
            "battery": {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"},
        }
