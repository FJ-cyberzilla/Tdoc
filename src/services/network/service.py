"""
TDoc Network Subsystem - Dynamic State Mapping
"""

import socket
import urllib.error
import urllib.request
from typing import Any, NamedTuple

from src.interfaces import DiagnosticService
from src.services.network.sms import SMSChecker
from src.services.network.wifi import WifiChecker
from src.services.network_checkers import (
    DNSChecker,
    HotspotChecker,
    NetworkSpeedChecker,
    ProxyChecker,
    RoutingTopologyChecker,
    TelephonyChecker,
    VPNStatusChecker,
)


class MirrorResult(NamedTuple):
    """Result of a mirror connectivity check."""

    online: bool
    details: str


class NetworkService(DiagnosticService):
    """Service to evaluate network connectivity and state."""

    def __init__(self) -> None:
        self._checkers: dict[str, Any] = {
            "dns": DNSChecker(),
            "topology": RoutingTopologyChecker(),
            "vpn": VPNStatusChecker(),
            "hotspot": HotspotChecker(),
            "telephony": TelephonyChecker(),
            "proxy": ProxyChecker(),
            "speed": NetworkSpeedChecker(),
            "wifi": WifiChecker(),
            "sms": SMSChecker(),
        }

    def run(self) -> dict[str, Any]:
        """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
        mirror: MirrorResult = self._check_termux_mirrors()

        return {
            "topology": self._checkers["topology"].check(),
            "local_ip": self._get_local_ip(),
            "dns": self._checkers["dns"].check(),
            "hotspot": self._checkers["hotspot"].check(),
            "vpn": self._checkers["vpn"].check(),
            "telephony": self._checkers["telephony"].check(),
            "proxy": self._checkers["proxy"].check(),
            "speed": self._checkers["speed"].check(),
            "wifi": self._checkers["wifi"].check(),
            "sms": self._checkers["sms"].check(),
            "mirror": {
                "online": mirror.online,
                "details": mirror.details,
            },
        }

    def _get_local_ip(self) -> str:
        """Finds the primary local IP address."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1.0)
                # Doesn't need to be reachable, just triggers routing logic
                s.connect(("8.8.8.8", 80))
                local_ip: str = s.getsockname()[0]
                return local_ip
        except (TimeoutError, OSError):
            return "127.0.0.1"

    def _check_termux_mirrors(self) -> MirrorResult:
        """Iterates through an array of redundant mirror nodes until a valid link is established."""
        mirrors = [
            "https://packages.termux.dev",
            "https://packages.termux.org",
            "https://mirror.accum.se",
            "https://mirror.mwt.me",
        ]

        for url in mirrors:
            try:
                with urllib.request.urlopen(url, timeout=2.0) as _:
                    pass
                domain: str = url.replace("https://", "")
                return MirrorResult(True, domain)
            except (urllib.error.URLError, TimeoutError):
                continue

        return MirrorResult(False, "All mirror nodes timed out")
