"""
TDoc Hardware Subsystem - System Storage Benchmarks & Clean API Battery Telemetry
"""

from src.interfaces import DiagnosticService
from src.services.storage import StorageMonitor
from src.services.battery import BatteryMonitor


class HealthService(DiagnosticService):
    """Service to evaluate hardware and storage health."""

    def __init__(self) -> None:
        self._storage = StorageMonitor()
        self._battery = BatteryMonitor()

    def run(self) -> dict:
        """Evaluates storage and battery metrics."""
        results = self._storage.run()
        results["battery"] = self._battery.run()

        return results
