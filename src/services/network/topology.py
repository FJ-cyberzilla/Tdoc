import subprocess
from typing import Any


class RoutingTopologyChecker:
    """
    Analyzes the network routing table to determine active interfaces and fabric.
    """

    def check(self) -> dict[str, Any]:
        """
        Analyzes the system routing table.

        Returns:
            dict: Topology info (wifi_active, fabric, interface).
        """
        topo = {"wifi_active": False, "fabric": "CELLULAR", "interface": "NONE"}
        try:
            res = subprocess.run(
                ["ip", "route", "show"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                return self._parse_ip_route(res.stdout)
        except (subprocess.SubprocessError, OSError):
            pass
        return topo

    def _parse_ip_route(self, output: str) -> dict[str, Any]:
        """Parses the output of 'ip route show'."""
        topo = {"wifi_active": False, "fabric": "CELLULAR", "interface": "NONE"}
        for line in output.splitlines():
            if "default" in line:
                self._update_topology_from_line(topo, line)
                break
        return topo

    def _update_topology_from_line(self, topo: dict[str, Any], line: str):
        """Updates topology dictionary based on a single route line."""
        if "wlan" in line:
            topo["wifi_active"] = True
            topo["fabric"] = "WI-FI"
        elif any(c in line for c in ["rmnet", "ccmni", "rndis", "p2p"]):
            topo["fabric"] = "CELLULAR"
