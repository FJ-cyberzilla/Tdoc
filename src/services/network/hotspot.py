import subprocess
from typing import Any


class HotspotChecker:
    """
    Checks if the device is currently acting as a hotspot.
    """

    def check(self) -> dict[str, Any]:
        """
        Checks for active hotspot interfaces and returns status details.
        """
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()

                active = []
                if "ap0" in output:
                    active.append("Wi-Fi Hotspot")
                if "rndis" in output:
                    active.append("USB Tethering")

                if active:
                    return {"active": True, "type": ", ".join(active)}

                return {"active": False, "type": "None"}
        except (subprocess.SubprocessError, OSError):
            pass
        return {"active": False, "type": "Error"}
