"""
Battery Diagnostic Service
"""

import json
import os
import shutil
import subprocess
from src.interfaces import DiagnosticService


class BatteryMonitor(DiagnosticService):
    """Monitors device battery health."""

    def run(self) -> dict[str, str]:
        """Queries battery statistics."""
        return self._get_battery_metrics()

    def _get_battery_metrics(self) -> dict[str, str]:
        """Queries official Termux API layers or falls back to sysfs."""
        metrics: dict[str, str] = {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"}

        # Mode 1: Intercept official unrooted Termux API system layer
        if shutil.which("termux-battery-status"):
            try:
                res = subprocess.run(
                    ["termux-battery-status"], capture_output=True, text=True, check=False
                )
                if res.returncode == 0:
                    data = json.loads(res.stdout)
                    metrics["capacity"] = f"{data.get('percentage', 'UNKNOWN')}%"
                    metrics["status"] = str(data.get("status", "UNKNOWN")).upper()

                    raw_temp = data.get("temperature", None)
                    if raw_temp is not None:
                        metrics["temp"] = f"{float(raw_temp):.1f}°C"
                    return metrics
            except Exception:
                pass

        # Mode 2: Absolute Fallback to raw legacy kernel paths if accessible
        base_path = "/sys/class/power_supply/battery"
        if os.path.exists(base_path):
            try:
                with open(os.path.join(base_path, "capacity"), "r", encoding="utf-8") as f:
                    metrics["capacity"] = f.read().strip() + "%"
                with open(os.path.join(base_path, "status"), "r", encoding="utf-8") as f:
                    metrics["status"] = f.read().strip().upper()
                with open(os.path.join(base_path, "temp"), "r", encoding="utf-8") as f:
                    metrics["temp"] = f"{float(f.read().strip()) / 10:.1f}°C"
            except (FileNotFoundError, PermissionError, ValueError, UnicodeDecodeError):
                pass

        return metrics
