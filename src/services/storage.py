"""
Storage Diagnostic Service
"""

import os
import shutil
import time
from typing import Any

from src.interfaces import DiagnosticService


class StorageMonitor(DiagnosticService):
    """Monitors storage health and performance."""

    def run(self) -> dict[str, Any]:
        """Evaluates free storage and write speed."""
        results: dict[str, Any] = {}

        # Disk usage
        try:
            _, _, free = shutil.disk_usage(".")
            results["free_storage_gb"] = free / (1024**3)
        except OSError:
            results["free_storage_gb"] = None

        # Write speed
        test_file: str = "io_perf.tmp"
        data: bytes = os.urandom(1024 * 1024 * 25)
        start: float = time.time()
        try:
            with open(test_file, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            delta: float = time.time() - start
            results["write_speed_mb_s"] = 25 / delta
            os.remove(test_file)
        except OSError:
            results["write_speed_mb_s"] = None

        return results
