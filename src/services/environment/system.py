import platform
import subprocess
from typing import Any


class SystemCollector:
    """Collects system information."""

    def _get_prop(self, key: str) -> str:
        """Natively resolves an Android system property value."""
        try:
            res: subprocess.CompletedProcess = subprocess.run(
                ["getprop", key], capture_output=True, text=True, check=False
            )
            return res.stdout.strip() if res.returncode == 0 else ""
        except Exception:
            return ""

    def get_android_environment(self) -> dict[str, Any]:
        return {
            "manufacturer": self._get_prop("ro.product.manufacturer").upper() or "ANDROID",
            "model": self._get_prop("ro.product.model") or "DEVICE",
            "version": self._get_prop("ro.build.version.release"),
            "sdk": self._get_prop("ro.build.version.sdk"),
            "build_id": self._get_prop("ro.build.id"),
        }

    def get_generic_environment(self) -> dict[str, Any]:
        return {
            "manufacturer": "Generic",
            "model": platform.system(),
            "version": platform.release(),
            "sdk": "N/A",
            "build_id": "STABLE_PC_INSTANCE",
        }
