import os
import platform
import re
import subprocess


class CPUCollector:
    """Collects CPU information."""

    def get_cpu_info(self) -> dict[str, str | int]:
        """Parses /proc/cpuinfo or falls back to nproc/platform for architecture."""
        cpu_info: dict[str, str | int] = {
            "arch": platform.machine(),
            "cores": 0,
            "model": "Unknown",
        }

        # Try parsing /proc/cpuinfo
        self._parse_cpuinfo(cpu_info)

        # Fallback for cores
        if cpu_info["cores"] == 0:
            self._set_cpu_cores_fallback(cpu_info)

        return cpu_info

    def _parse_cpuinfo(self, cpu_info: dict[str, str | int]) -> None:
        try:
            with open("/proc/cpuinfo") as f:
                content: str = f.read()
                model_match = re.search(r"Hardware\s*:\s*(.+)", content)
                cpu_info["model"] = model_match.group(1).strip() if model_match else "Android"
                cpu_info["cores"] = len(re.findall(r"processor\s*:", content))
        except Exception:
            pass

    def _set_cpu_cores_fallback(self, cpu_info: dict[str, str | int]) -> None:
        try:
            cpu_info["cores"] = int(subprocess.check_output(["nproc"], text=True).strip())
        except Exception:
            cpu_info["cores"] = os.cpu_count() or 8
