import json
import subprocess
from typing import Any


class WifiChecker:
    """Retrieves Wi-Fi connection information with enhanced status detection."""

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

                # Determine state
                state = data.get("supplicant_state", "UNKNOWN")
                if state == "UNINITIALIZED":
                    data["status"] = "OFF"
                elif state == "DISCONNECTED" or data.get("ip") == "0.0.0.0":
                    data["status"] = "DISCONNECTED"
                else:
                    data["status"] = "CONNECTED"
                return data
            return {"status": "ERROR"}
        except Exception:
            return {"status": "ERROR"}
