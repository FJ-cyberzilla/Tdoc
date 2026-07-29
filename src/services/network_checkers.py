"""
Network diagnostic and information services for the Termux environment.

This module is now deprecated and acts as a compatibility layer for
`src.services.network`. Please use `src.services.network` directly.
"""

from src.services.network.base import NetworkChecker
from src.services.network.dns import DNSChecker
from src.services.network.geo import IPGeolocationService
from src.services.network.hotspot import HotspotChecker
from src.services.network.proxy import ProxyChecker
from src.services.network.speed import NetworkSpeedChecker
from src.services.network.telephony import TelephonyChecker
from src.services.network.topology import RoutingTopologyChecker
from src.services.network.vpn import VPNStatusChecker

__all__ = [
    "IPGeolocationService",
    "DNSChecker",
    "RoutingTopologyChecker",
    "VPNStatusChecker",
    "HotspotChecker",
    "TelephonyChecker",
    "ProxyChecker",
    "NetworkSpeedChecker",
    "NetworkChecker",
]
