"""
TDoc Network Subsystem - Dynamic State Mapping
"""

import asyncio
import socket
import urllib.error
import urllib.request
from typing import Any, NamedTuple

from src.interfaces import AsyncDiagnosticService
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


class NetworkService(AsyncDiagnosticService):
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

    async def run(self) -> dict[str, Any]:
        """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
        mirror: MirrorResult = await asyncio.to_thread(self._check_termux_mirrors)

        # Run checkers in parallel
        results = await asyncio.gather(
            asyncio.to_thread(self._checkers["topology"].check),
            asyncio.to_thread(self._checkers["dns"].check),
            asyncio.to_thread(self._checkers["hotspot"].check),
            asyncio.to_thread(self._checkers["vpn"].check),
            asyncio.to_thread(self._checkers["telephony"].check),
            asyncio.to_thread(self._checkers["proxy"].check),
            asyncio.to_thread(self._checkers["speed"].check),
            asyncio.to_thread(self._checkers["wifi"].check),
            asyncio.to_thread(self._checkers["sms"].check),
        )

        return {
            "topology": results[0],
            "local_ip": await asyncio.to_thread(self._get_local_ip),
            "dns": results[1],
            "hotspot": results[2],
            "vpn": results[3],
            "telephony": results[4],
            "proxy": results[5],
            "speed": results[6],
            "wifi": results[7],
            "sms": results[8],
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
