"""
Battery Diagnostic Service
"""

import json
import os
import shutil
import subprocess
from typing import Any

from src.interfaces import DiagnosticService


class BatteryMonitor(DiagnosticService):
    """Monitors device battery health."""

    def run(self) -> dict[str, str]:
        """Queries battery statistics."""
        return self._get_battery_metrics()

    def _get_battery_metrics(self) -> dict[str, Any]:
        """Queries official Termux API layers or falls back to sysfs."""
        # Attempt Termux API
        termux_data: dict[str, Any] | None = self._get_termux_battery_data()
        if termux_data:
            return termux_data

        # Fallback diagnostics if API fails
        return {
            "capacity": "0%",
            "status": "DISCONNECTED",
            "temp": "0.0°C",
            "cap_num": 0,
            "temp_num": 0.0,
            "voltage": 0.0,
            "current": 0.0,
            "wattage": 0.0,
        }

    def _get_termux_battery_data(self) -> dict[str, Any] | None:
        if not shutil.which("termux-battery-status"):
            return None
        try:
            res: subprocess.CompletedProcess = subprocess.run(
                ["termux-battery-status"], capture_output=True, text=True, check=False
            )
            if res.returncode == 0:
                data: dict[str, Any] = json.loads(res.stdout)

                # Robust parsing with sensible fallbacks
                cap = int(data.get("percentage", 0))
                # Status mapping
                status = str(data.get("status", "DISCHARGING")).upper()

                # Temperature in Celsius (sometimes returned in tenths of C)
                raw_temp = data.get("temperature", 0)
                temp = float(raw_temp)
                if temp > 100:  # Heuristic: if > 100, likely tenths of Celsius
                    temp /= 10.0

                # Wattage calculation
                # Termux API might return 'current_now' in microAmps or similar
                voltage_uV = float(data.get("voltage", 0))
                current_uA = float(data.get("current_now", 0))

                # Convert to Volts and Amps (standard units)
                voltage = voltage_uV / 1000000
                current = current_uA / 1000000
                wattage = voltage * current

                return {
                    "capacity": f"{cap}%",
                    "status": status,
                    "temp": f"{temp:.1f}°C",
                    "cap_num": cap,
                    "temp_num": temp,
                    "voltage": voltage,
                    "current": current,
                    "wattage": wattage,
                }
        except (json.JSONDecodeError, subprocess.SubprocessError, ValueError, TypeError):
            pass
        return None

    def _get_sysfs_battery_data(self, metrics: dict[str, str]) -> dict[str, str]:
        base_path: str = "/sys/class/power_supply/battery"
        if os.path.exists(base_path):
            try:
                with open(os.path.join(base_path, "capacity"), encoding="utf-8") as f:
                    metrics["capacity"] = f.read().strip() + "%"
                with open(os.path.join(base_path, "status"), encoding="utf-8") as f:
                    metrics["status"] = f.read().strip().upper()
                with open(os.path.join(base_path, "temp"), encoding="utf-8") as f:
                    metrics["temp"] = f"{float(f.read().strip()) / 10:.1f}°C"
            except (FileNotFoundError, PermissionError, ValueError, UnicodeDecodeError):
                pass
        return metrics
