"""
System Service for querying memory, process statistics, and dumpsys.
"""

from src.core.command_runner import CommandRunner
from src.interfaces import DiagnosticService


class SystemService(DiagnosticService):
    """Provides comprehensive system diagnostics."""

    def __init__(self):
        self.runner = CommandRunner()

    def run(self) -> dict:
        """Aggregates system data."""
        return {
            "uptime": self.runner.run_command(["uptime"]),
            "ps": self.runner.run_command(["ps", "aux"]),
            "disk": self.runner.run_command(["df", "-h"]),
            "dumpsys_battery": self.runner.run_command(["dumpsys", "battery"]),
        }
