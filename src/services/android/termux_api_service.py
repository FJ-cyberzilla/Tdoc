"""
Termux API Service for querying Termux-specific sensors and info.
"""

from src.core.command_runner import CommandRunner
from src.interfaces import DiagnosticService


class TermuxApiService(DiagnosticService):
    """Provides Termux API diagnostics."""

    def __init__(self):
        self.runner = CommandRunner()

    def trigger_haptic(self, duration_ms: int = 100):
        """Triggers haptic feedback."""
        return self.runner.run_command(["termux-vibrate", "-d", str(duration_ms)])

    def toggle_wifi(self, state: bool):
        """Toggles Wi-Fi on or off."""
        # Note: Termux doesn't directly toggle Wi-Fi in the standard API.
        # This is a placeholder for potential integration if supported by plugins.
        return {
            "status": "NOT_SUPPORTED",
            "message": "Wi-Fi toggling not supported in standard Termux API",
        }

    def toggle_location(self, state: bool):
        """Toggles Location services (GPS) on or off."""
        # Note: Termux doesn't directly toggle GPS in the standard API.
        # This is a placeholder.
        return {
            "status": "NOT_SUPPORTED",
            "message": "GPS toggling not supported in standard Termux API",
        }

    def run(self) -> dict:
        """Aggregates comprehensive Termux API data."""
        return {
            "battery": self.runner.run_command(["termux-battery-status"]),
            "wifi": self.runner.run_command(["termux-wifi-connectioninfo"]),
            "telephony": self.runner.run_command(["termux-telephony-deviceinfo"]),
            "location": self.runner.run_command(["termux-location"]),
        }
