"""
Storage Diagnostic Service
"""

import os
import shutil
import time

from src.interfaces import DiagnosticService


class StorageMonitor(DiagnosticService):
    """Monitors storage health and performance."""

    def run(self) -> dict:
        """Evaluates free storage and write speed."""
        results = {}

        # Disk usage
        try:
            _, _, free = shutil.disk_usage(".")
            results["free_storage_gb"] = free / (1024**3)
        except Exception:
            results["free_storage_gb"] = None

        # Write speed
        test_file = "io_perf.tmp"
        data = os.urandom(1024 * 1024 * 25)
        start = time.time()
        try:
            with open(test_file, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            delta = time.time() - start
            results["write_speed_mb_s"] = 25 / delta
            os.remove(test_file)
        except Exception:
            results["write_speed_mb_s"] = None

        return results
