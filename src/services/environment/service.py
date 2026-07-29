"""
Environment Service - Main entry point.
"""

import os
import platform
import shutil
from typing import Any

from .cpu import CPUCollector
from .ram import RAMCollector
from .system import SystemCollector
from .uptime import UptimeCollector


class EnvironmentService:
    """Service to evaluate environmental properties."""

    def __init__(self) -> None:
        self.cpu_collector = CPUCollector()
        self.ram_collector = RAMCollector()
        self.uptime_collector = UptimeCollector()
        self.system_collector = SystemCollector()

    def run(self) -> dict[str, Any]:
        """Evaluates cross-platform environmental properties and ecosystem status."""
        return self._run_environment_checks()

    def _run_environment_checks(self) -> dict[str, Any]:
        is_android: bool = bool(shutil.which("getprop"))

        results: dict[str, Any] = {
            "is_android": is_android,
            "platform_system": platform.system(),
            "platform_machine": platform.machine(),
            "uptime": self.uptime_collector.get_uptime(),
            "cpu": self.cpu_collector.get_cpu_info(),
            "ram": self.ram_collector.get_ram_info(),
        }

        if is_android:
            results.update(self.system_collector.get_android_environment())
        else:
            results.update(self.system_collector.get_generic_environment())

        results["lang"] = os.environ.get("LANG", "en_US.UTF-8")
        results["api_connected"] = bool(shutil.which("termux-battery-status"))
        results["boot_status"] = os.path.exists("/data/data/com.termux/files/home/.termux/boot")

        return results
