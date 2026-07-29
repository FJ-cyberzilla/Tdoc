"""
Command Handlers for UI actions.
"""

from abc import ABC, abstractmethod
from typing import Any


class CommandHandler(ABC):
    """Abstract base class for command handlers."""

    def __init__(self, renderer: Any):
        self.renderer = renderer

    @abstractmethod
    def handle(self, result: Any):
        """Handles the command result."""
        pass


class DashboardHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_dashboard(
            result["platform"]["environment"], result["network"], result["health"]
        )


class NetworkHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_network_metrics(result)


class SecurityHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_security_metrics(result)


class UpdaterHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_updater_metrics(result)


class PackageManagerHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_package_manager(result)
