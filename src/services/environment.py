"""
TDoc Environment Subsystem - System Profiler & Termux Ecosystem Analysis
"""

import os
import platform
import re
import shutil
import subprocess


class EnvironmentService:
    """Service to evaluate environmental properties."""

    def run(self) -> dict:
        """Evaluates cross-platform environmental properties and ecosystem status."""
        return self._run_environment_checks()

    def _get_prop(self, key: str) -> str:
        """Natively resolves an Android system property value."""
        try:
            res = subprocess.run(["getprop", key], capture_output=True, text=True, check=False)
            return res.stdout.strip() if res.returncode == 0 else ""
        except Exception:
            return ""

    def _get_cpu_info(self) -> dict:
        """Parses /proc/cpuinfo or falls back to nproc/platform for architecture."""
        cpu_info = {"arch": platform.machine(), "cores": 0, "model": "Unknown"}
        try:
            with open("/proc/cpuinfo", "r") as f:
                content = f.read()
                model_match = re.search(r"Hardware\s*:\s*(.+)", content)
                cpu_info["model"] = model_match.group(1).strip() if model_match else "Android"

                cpu_info["cores"] = len(re.findall(r"processor\s*:", content))
        except Exception:
            pass

        if cpu_info["cores"] == 0:
            try:
                cpu_info["cores"] = int(subprocess.check_output(["nproc"], text=True).strip())
            except Exception:
                cpu_info["cores"] = os.cpu_count() or 8

        return cpu_info

    def _get_uptime(self) -> str:
        """Parses /proc/uptime for system uptime."""
        try:
            # Try `uptime` command first if available
            output = subprocess.check_output(["uptime"], text=True)
            match = re.search(r"up\s+(.*?)(?:,|\s+user)", output)
            if match:
                return match.group(1).strip()
        except Exception:
            pass

        try:
            # Fallback to /proc/uptime
            with open("/proc/uptime", "r") as f:
                seconds = float(f.read().split()[0])
                days = int(seconds // 86400)
                hours = int((seconds % 86400) // 3600)
                minutes = int((seconds % 3600) // 60)

                parts = []
                if days > 0:
                    parts.append(f"{days}d")
                if hours > 0:
                    parts.append(f"{hours}h")
                if minutes > 0:
                    parts.append(f"{minutes}m")
                return " ".join(parts) if parts else "Just started"
        except Exception:
            return "UNKNOWN"

    def _get_ram_info(self) -> dict:
        """Parses /proc/meminfo for RAM metrics in GB."""
        ram = {"total": 0.0, "available": 0.0, "percent": 0.0}
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = {}
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        value = parts[1].split()[0].strip()
                        meminfo[name] = int(value)

                total = meminfo.get("MemTotal", 0)
                available = meminfo.get("MemAvailable", meminfo.get("MemFree", 0))

                if total > 0:
                    ram["total"] = total / (1024 * 1024)  # GB
                    ram["available"] = available / (1024 * 1024)  # GB
                    ram["used"] = ram["total"] - ram["available"]
                    ram["percent"] = (ram["used"] / ram["total"]) * 100
        except Exception:
            pass
        return ram

    def _run_environment_checks(self) -> dict:
        is_android = bool(shutil.which("getprop"))

        results = {
            "is_android": is_android,
            "platform_system": platform.system(),
            "platform_machine": platform.machine(),
            "uptime": self._get_uptime(),
            "cpu": self._get_cpu_info(),
            "ram": self._get_ram_info(),
        }

        if is_android:
            results["manufacturer"] = self._get_prop("ro.product.manufacturer").upper() or "ANDROID"
            results["model"] = self._get_prop("ro.product.model") or "DEVICE"
            results["version"] = self._get_prop("ro.build.version.release")
            results["sdk"] = self._get_prop("ro.build.version.sdk")
            results["build_id"] = self._get_prop("ro.build.id")
        else:
            results["manufacturer"] = "Generic"
            results["model"] = platform.system()
            results["version"] = platform.release()
            results["sdk"] = "N/A"
            results["build_id"] = "STABLE_PC_INSTANCE"

        results["lang"] = os.environ.get("LANG", "en_US.UTF-8")
        results["api_connected"] = bool(shutil.which("termux-battery-status"))
        results["boot_status"] = os.path.exists("/data/data/com.termux/files/home/.termux/boot")

        return results
