"""
Device Service for querying property and hardware information.
"""

from src.core.command_runner import CommandRunner
from src.interfaces import DiagnosticService


class DeviceService(DiagnosticService):
    """Provides hardware and system properties."""

    def __init__(self):
        self.runner = CommandRunner()

    def run(self) -> dict:
        """Aggregates comprehensive device property data."""
        # Property keys to query
        props = [
            "ro.product.model",
            "ro.product.manufacturer",
            "ro.product.brand",
            "ro.product.device",
            "ro.build.version.release",
            "ro.build.version.sdk",
            "ro.hardware",
            "ro.board.platform",
            "ro.soc.model",
        ]

        data = {prop: self.runner.run_command(["getprop", prop]) for prop in props}

        # Add additional hardware info
        data["cpuinfo"] = self.runner.run_command(["cat", "/proc/cpuinfo"])
        data["meminfo"] = self.runner.run_command(["cat", "/proc/meminfo"])

        return data
