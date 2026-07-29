"""
Command Handlers for UI actions.
"""

from abc import ABC, abstractmethod
from typing import Any

# Import specialized handlers from their own modules
from .dashboard import DashboardHandler as DashboardHandler
from .network import NetworkHandler as NetworkHandler
from .sensor import SensorHandler as SensorHandler


class CommandHandler(ABC):
    """Abstract base class for command handlers."""

    def __init__(self, renderer: Any, router: Any):
        self.renderer = renderer
        self.router = router

    @abstractmethod
    def handle(self, result: Any):
        """Handles the command result."""
        pass


class SecurityHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_security_metrics(result)


class UpdaterHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_updater_metrics(result)


class PackageManagerHandler(CommandHandler):
    def handle(self, result: dict):
        self.renderer.render_package_manager(result)
