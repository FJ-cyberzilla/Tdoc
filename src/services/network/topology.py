import subprocess
from dataclasses import dataclass
from enum import Enum, auto


class NetworkFabric(Enum):
    CELLULAR = auto()
    WIFI = auto()
    UNKNOWN = auto()

@dataclass(frozen=True)
class TopologyInfo:
    wifi_active: bool
    fabric: NetworkFabric
    interface: str

class RoutingTopologyChecker:
    """
    Analyzes the network routing table to determine active interfaces and fabric.
    """

    def check(self) -> TopologyInfo:
        """
        Analyzes the system routing table.

        Returns:
            TopologyInfo: Topology info (wifi_active, fabric, interface).
        """
        topo = TopologyInfo(
            wifi_active=False,
            fabric=NetworkFabric.CELLULAR,
            interface="NONE"
        )
        try:
            res = subprocess.run(
                ["ip", "route", "show"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                return self._parse_ip_route(res.stdout)
        except (subprocess.SubprocessError, OSError):
            pass
        return topo

    def _parse_ip_route(self, output: str) -> TopologyInfo:
        """Parses the output of 'ip route show'."""
        wifi_active = False
        fabric = NetworkFabric.CELLULAR
        interface = "NONE"

        for line in output.splitlines():
            if "default" in line:
                if "wlan" in line:
                    wifi_active = True
                    fabric = NetworkFabric.WIFI
                elif any(c in line for c in ["rmnet", "ccmni", "rndis", "p2p"]):
                    fabric = NetworkFabric.CELLULAR
                break
        return TopologyInfo(wifi_active=wifi_active, fabric=fabric, interface=interface)
