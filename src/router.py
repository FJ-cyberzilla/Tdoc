"""
TDoc Router - Centralized Orchestration Layer.
"""

from typing import Any, Dict
from src.exceptions import RouterError
from src.interfaces import DiagnosticService


class TDocRouter:
    """Orchestrates requests between the UI and system modules."""

    def __init__(self, services: Dict[str, DiagnosticService]):
        """
        Initializes the router with necessary services.

        Args:
            services: A dictionary containing diagnostic service instances.
        """
        self.services = services

    def route_action(self, action_id: str) -> Any:
        """
        Routes an action request to the appropriate service.

        Args:
            action_id: The identifier for the action to route.

        Returns:
            The result of the action.

        Raises:
            RouterError: If the action is unknown or an error occurs.
        """
        try:
            if action_id == "platform":
                return self.services["platform"].run()
            if action_id in ["network", "security", "updater"]:
                return self.services[action_id].run()
            raise RouterError(f"Unknown action ID: {action_id}")
        except Exception as e:
            raise RouterError(f"Error routing action '{action_id}': {e}") from e

    def get_basic_info(self) -> Dict[str, Any]:
        """Provides basic system information for the HUD."""
        # For now, return placeholder data.
        return {
            "device": "TDoc System",
            "battery": {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"},
        }
