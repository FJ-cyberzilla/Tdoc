"""
Network Service for querying network interface and connectivity information.
"""

from src.core.command_runner import CommandRunner
from src.interfaces import DiagnosticService


class NetworkService(DiagnosticService):
    """Provides network diagnostics."""

    def __init__(self):
        self.runner = CommandRunner()

    def run(self) -> dict:
        """Aggregates comprehensive network data."""
        return {
            "interfaces": self.runner.run_command(["ip", "addr"]),
            "routes": self.runner.run_command(["ip", "route"]),
            "netstat": self.runner.run_command(["netstat", "-tulpn"]),
        }
