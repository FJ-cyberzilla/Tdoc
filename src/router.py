"""
TDoc Router - Centralized Orchestration Layer.
"""

import functools
from collections.abc import Callable
from typing import Any

from src.exceptions import RouterError, TDocError
from src.interfaces import DiagnosticService


class TDocRouter:
    """Orchestrates requests between the UI and system modules."""

    def __init__(self, services: dict[str, DiagnosticService] | None = None):
        """
        Initializes the router with necessary services.

        Args:
            services: A dictionary containing diagnostic service instances.
        """
        self.services: dict[str, dict[str, Any]] = {}
        self.composite_actions: dict[str, Callable] = {}
        if services:
            for name, service in services.items():
                self.register_service(name, service)
        self.middlewares: list[Any] = []

    def register_service(self, name: str, service: DiagnosticService, priority: int = 0):
        """Registers a new service with an optional priority."""
        self.services[name] = {"service": service, "priority": priority}

    def register_composite_action(self, name: str, action_func: Callable):
        """Registers a new composite action."""
        self.composite_actions[name] = action_func

    def add_middleware(self, middleware_fn: Any):
        """Adds a middleware function to the routing pipeline."""
        self.middlewares.append(middleware_fn)

    def route_action(self, action_id: str) -> Any:
        """
        Routes an action request to the appropriate service, applying middlewares.
        """
        if action_id in self.composite_actions:
            return self.composite_actions[action_id](self)

        service_entry = self.services.get(action_id)
        if not service_entry:
            raise RouterError(f"Unknown action ID: {action_id}")

        service = service_entry["service"]

        def final_handler(aid: str) -> Any:
            try:
                return service.run()
            except TDocError:
                # Re-raise known TDoc errors
                raise
            except Exception as e:
                # Wrap unknown errors
                raise RouterError(
                    f"Error executing action '{aid}': {e}", context={"original_error": str(e)}
                ) from e

        # Pipeline execution (middleware chain)
        handler = final_handler

        def create_handler(aid, m, h):
            return m(aid, h)

        for middleware in reversed(self.middlewares):
            current_handler = handler
            handler = functools.partial(create_handler, m=middleware, h=current_handler)

        return handler(action_id)

    def get_basic_info(self) -> dict[str, Any]:
        """Provides basic system information for the HUD."""
        try:
            health = self.route_action("health")
            battery = health.get("battery", {})
            return {
                "device": "TDoc System",
                "battery": {
                    "capacity": battery.get("capacity", "UNKNOWN"),
                    "temp": battery.get("temp", "UNKNOWN"),
                    "status": battery.get("status", "UNKNOWN"),
                },
            }
        except (RouterError, KeyError):
            return {
                "device": "TDoc System",
                "battery": {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"},
            }
