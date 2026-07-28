"""
TDoc Network Subsystem - Dynamic State Mapping
"""

import socket
import urllib.request
from typing import NamedTuple

from src.interfaces import DiagnosticService
from src.services.network_checkers import (
    DNSChecker,
    HotspotChecker,
    RoutingTopologyChecker,
    VPNStatusChecker,
)


class MirrorResult(NamedTuple):
    """Result of a mirror connectivity check."""

    online: bool
    details: str


class NetworkService(DiagnosticService):
    """Service to evaluate network connectivity and state."""

    def __init__(self):
        self._checkers = {
            "dns": DNSChecker(),
            "topology": RoutingTopologyChecker(),
            "vpn": VPNStatusChecker(),
            "hotspot": HotspotChecker(),
        }

    def run(self) -> dict:
        """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
        mirror = self._check_termux_mirrors()
        return {
            "topology": self._checkers["topology"].check(),
            "local_ip": self._get_local_ip(),
            "dns": self._checkers["dns"].check(),
            "hotspot_active": self._checkers["hotspot"].check(),
            "vpn": self._checkers["vpn"].check(),
            "mirror": {
                "online": mirror.online,
                "details": mirror.details,
            },
        }

    def _get_local_ip(self) -> str:
        """Finds the primary local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't need to be reachable, just triggers routing logic
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
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
                domain = url.replace("https://", "")
                return MirrorResult(True, domain)
            except (urllib.error.URLError, TimeoutError):
                continue

        return MirrorResult(False, "All mirror nodes timed out")
