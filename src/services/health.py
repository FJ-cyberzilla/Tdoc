"""
TDoc Hardware Subsystem - System Storage Benchmarks & Clean API Battery Telemetry
"""

import shutil
from typing import Any

from src.interfaces import DiagnosticService
from src.services.battery import BatteryMonitor
from src.services.storage import StorageMonitor


class HealthService(DiagnosticService):
    """Service to evaluate hardware and storage health."""

    def __init__(self) -> None:
        self._storage = StorageMonitor()
        self._battery = BatteryMonitor()

    def run(self) -> dict[str, Any]:
        """Evaluates storage and battery metrics."""
        results: dict[str, Any] = self._storage.run()
        # Add used storage
        total, _, free = shutil.disk_usage(".")
        results["used_storage_gb"] = (total - free) / (1024**3)
        results["total_storage_gb"] = total / (1024**3)
        results["battery"] = self._battery.run()

        return results
