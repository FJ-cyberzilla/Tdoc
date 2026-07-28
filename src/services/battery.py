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

        # Attempt Termux API
        termux_data = self._get_termux_battery_data()
        if termux_data:
            return termux_data

        # Absolute Fallback to raw legacy kernel paths
        return self._get_sysfs_battery_data(metrics)

    def _get_termux_battery_data(self) -> dict[str, str] | None:
        if not shutil.which("termux-battery-status"):
            return None
        try:
            res = subprocess.run(
                ["termux-battery-status"], capture_output=True, text=True, check=False
            )
            if res.returncode == 0:
                data = json.loads(res.stdout)
                return {
                    "capacity": f"{data.get('percentage', 'UNKNOWN')}%",
                    "status": str(data.get("status", "UNKNOWN")).upper(),
                    "temp": f"{float(data.get('temperature', 0)):.1f}°C"
                    if data.get("temperature") is not None
                    else "UNKNOWN",
                }
        except Exception:
            pass
        return None

    def _get_sysfs_battery_data(self, metrics: dict[str, str]) -> dict[str, str]:
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
