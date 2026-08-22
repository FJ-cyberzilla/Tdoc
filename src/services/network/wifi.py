import json
import subprocess
from typing import Any


class WifiChecker:
    """Retrieves Wi-Fi connection information with enhanced status detection."""

    def _determine_status(self, data: dict[str, Any]) -> str:
        """Determines Wi-Fi status based on connection data."""
        state = data.get("supplicant_state", "UNKNOWN")
        if state == "UNINITIALIZED":
            return "OFF"
        if state == "DISCONNECTED" or data.get("ip") == "0.0.0.0":
            return "DISCONNECTED"
        return "CONNECTED"

    def check(self) -> dict[str, Any]:
        try:
            res = subprocess.run(
                ["termux-wifi-connectioninfo"],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            )
            if res.returncode == 0:
                data = json.loads(res.stdout)
                data["status"] = self._determine_status(data)
                return data
            return {"status": "ERROR"}
        except Exception:
            return {"status": "ERROR"}
