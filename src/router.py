"""
TDoc Router - Centralized Orchestration Layer.
"""

import functools
from collections.abc import Callable
from typing import Any

from src.exceptions import RouterError, TDocError


class TDocRouter:
    """Orchestrates requests between the UI handlers and system services."""

    def __init__(self, services: dict[str, Any] | None = None):
        """
        Initializes the router with optional initial services.

        Args:
            services: Dict mapping action/service names to service instances.
        """
        self.services: dict[str, dict[str, Any]] = {}
        self.composite_actions: dict[str, Callable] = {}
        self.middlewares: list[Any] = []

        if services:
            for name, service in services.items():
                self.register_service(name, service)

    def register_service(self, name: str, service: Any, priority: int = 0) -> None:
        """Registers a service (DiagnosticService or TelemetryService) with priority."""
        self.services[name] = {"service": service, "priority": priority}

    def register_composite_action(self, name: str, action_func: Callable) -> None:
        """Registers a new composite action handler."""
        self.composite_actions[name] = action_func

    def add_middleware(self, middleware_fn: Any) -> None:
        """Adds a middleware function to the routing execution pipeline."""
        self.middlewares.append(middleware_fn)

    def route_action(self, action_id: str) -> Any:
        """
        Routes an action request to the registered service or composite action,
        applying all middleware layers in sequence.
        """
        if action_id in self.composite_actions:
            return self.composite_actions[action_id](self)

        service_entry = self.services.get(action_id)
        if not service_entry:
            raise RouterError(f"Unknown action ID: '{action_id}'")

        service = service_entry["service"]

        def final_handler(aid: str) -> Any:
            try:
                # Fulfill TelemetryService interface if available, else DiagnosticService
                if hasattr(service, "get_telemetry"):
                    return service.get_telemetry()
                elif hasattr(service, "run"):
                    return service.run()
                else:
                    raise RouterError(
                        f"Service '{aid}' implements no recognized execution protocol."
                    )
            except TDocError:
                raise
            except Exception as e:
                raise RouterError(
                    f"Error executing action '{aid}': {e}", context={"original_error": str(e)}
                ) from e

        # Build middleware pipeline bottom-up
        handler = final_handler
        for middleware in reversed(self.middlewares):
            current_handler = handler
            handler = functools.partial(
                lambda aid, m, h: m(aid, h), m=middleware, h=current_handler
            )

        return handler(action_id)

    # =========================================================================
    # Telemetry Convenience Proxies (Used by UI Handlers)
    # =========================================================================

    def get_environment_telemetry(self) -> dict[str, Any]:
        """Fetches CPU, RAM, and OS uptime telemetry."""
        try:
            return self.route_action("environment")
        except RouterError:
            return {}

    def get_health_telemetry(self) -> dict[str, Any]:
        """Fetches battery, thermal, and storage telemetry."""
        try:
            return self.route_action("health")
        except RouterError:
            return {}

    def get_network_telemetry(self) -> dict[str, Any]:
        """Fetches DNS, VPN, and cellular telemetry."""
        try:
            return self.route_action("network")
        except RouterError:
            return {}

    def get_security_telemetry(self) -> dict[str, Any]:
        """Fetches Root, SELinux, and SUID audit telemetry."""
        try:
            return self.route_action("security")
        except RouterError:
            return {}

    def get_sensor_hub_telemetry(self) -> dict[str, Any]:
        """Fetches modular sensor data and activity detection."""
        try:
            return self.route_action("sensor_hub")
        except RouterError:
            return {}
