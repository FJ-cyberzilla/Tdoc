import json
import subprocess
from typing import Any


class TelephonyChecker:
    """
    Retrieves telephony and cellular network information using termux-telephony tools.
    """

    def check(self) -> dict[str, Any]:
        """
        Performs telephony diagnostic checks.

        Returns:
            dict: Telephony data (deviceinfo, signalstrength, cellinfo).
        """
        data: dict[str, Any] = {}
        for cmd in ["deviceinfo", "signalstrength", "cellinfo"]:
            try:
                res = subprocess.run(
                    ["termux-telephony-" + cmd],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=2,
                )
                if res.returncode == 0:
                    data[cmd] = json.loads(res.stdout)
                else:
                    data[cmd] = {"error": "Permission denied or access error"}
            except Exception:
                # Common if Termux:API is not installed or permissions are missing
                data[cmd] = {"error": "Tool not found or execution failed"}
        return data
