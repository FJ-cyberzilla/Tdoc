import subprocess
from typing import Any

from .geo import IPGeolocationService


class VPNStatusChecker:
    """
    Detects if a VPN is active by checking network interfaces and public IP changes.
    """

    def __init__(self):
        self.geo_service = IPGeolocationService()

    def check(self) -> dict[str, Any]:
        """
        Retrieves comprehensive VPN status.

        Returns:
            dict: VPN status and geolocation details.
        """
        vpn_info: dict[str, Any] = {
            "active": False,
            "ip": "UNKNOWN",
            "country": "UNKNOWN",
            "isp": "UNKNOWN",
            "org": "UNKNOWN",
            "interface": "NONE",
        }
        # Check local interfaces first
        vpn_info["active"], vpn_info["interface"] = self._check_vpn_interfaces()

        # Augment with geolocation data (public-facing identity)
        details = self.geo_service.get_details()
        vpn_info.update(details)

        # If we have a public IP, we consider it 'active' network-wise
        if vpn_info["ip"] != "UNKNOWN":
            vpn_info["active"] = True

        return vpn_info

    def _check_vpn_interfaces(self) -> tuple[bool, str]:
        """Checks for common VPN interface names in 'ip link'."""
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()
                for iface in ["tun", "wg0", "ppp0"]:
                    if iface in output:
                        return True, iface.upper()
        except (subprocess.SubprocessError, OSError):
            pass
        return False, "NONE"
