import subprocess


class HotspotChecker:
    """
    Checks if the device is currently acting as a hotspot.
    """

    def check(self) -> bool:
        """
        Checks for active hotspot interfaces.

        Returns:
            bool: True if hotspot/tethering seems active.
        """
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()
                # ap0 for hotspot, rndis for USB tethering
                return "ap0" in output or "rndis" in output
        except (subprocess.SubprocessError, OSError):
            pass
        return False
