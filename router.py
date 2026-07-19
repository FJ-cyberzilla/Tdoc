"""
TDoc Router - Centralized Orchestration Layer.
"""

from typing import Any, Dict
from exceptions import RouterError

class TDocRouter:
    """Orchestrates requests between the UI and system modules."""

    def __init__(self, modules: Dict[str, Any]):
        """
        Initializes the router with necessary modules.
        
        Args:
            modules: A dictionary containing module instances.
        """
        self.modules = modules

    def route_action(self, action_id: str) -> Any:
        """
        Routes an action request to the appropriate module.

        Args:
            action_id: The identifier for the action to route.

        Returns:
            The result of the action.

        Raises:
            RouterError: If the action is unknown or an error occurs.
        """
        try:
            if action_id == "platform":
                self.modules["environment"].run_environment_checks()
                self.modules["health"].run_health_checks()
                return "Platform metrics collected."
            elif action_id == "network":
                return self.modules["network"].run_network_checks()
            elif action_id == "security":
                return self.modules["security"].run_security_checks()
            elif action_id == "updater":
                if hasattr(self.modules["updater"], "run_updater_checks"):
                    return self.modules["updater"].run_updater_checks()
                return "Workspace Core Index: Pristine."
            else:
                raise RouterError(f"Unknown action ID: {action_id}")
        except Exception as e:
            raise RouterError(f"Error routing action '{action_id}': {e}") from e

    def get_basic_info(self) -> Dict[str, Any]:
        """Provides basic system information for the HUD."""
        # For now, return placeholder data.
        return {
            "device": "TDoc System",
            "battery": {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"}
        }
