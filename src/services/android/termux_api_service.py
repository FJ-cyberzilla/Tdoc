"""
Termux API Service for querying Termux-specific sensors and info.
"""

from src.core.command_runner import CommandRunner
from src.interfaces import DiagnosticService


class TermuxApiService(DiagnosticService):
    """Provides Termux API diagnostics."""

    def __init__(self):
        self.runner = CommandRunner()

    def run(self) -> dict:
        """Aggregates comprehensive Termux API data."""
        return {
            "battery": self.runner.run_command(["termux-battery-status"]),
            "wifi": self.runner.run_command(["termux-wifi-connectioninfo"]),
            "telephony": self.runner.run_command(["termux-telephony-deviceinfo"]),
            "location": self.runner.run_command(["termux-location"]),
        }
