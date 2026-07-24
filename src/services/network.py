"""
TDoc Network Subsystem - Dynamic State Mapping
"""

import json
import socket
import subprocess
import urllib.request
from typing import NamedTuple
from src.interfaces import DiagnosticService


class MirrorResult(NamedTuple):
    """Result of a mirror connectivity check."""

    online: bool
    details: str


class NetworkService(DiagnosticService):
    """Service to evaluate network connectivity and state."""

    def run(self) -> dict:
        """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
        mirror = self._check_termux_mirrors()
        return {
            "topology": self._get_routing_topology(),
            "local_ip": self._get_local_ip(),
            "dns": self._get_dns_servers(),
            "hotspot_active": self._check_hotspot_status(),
            "vpn": self._check_vpn_status(),
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

    def _get_dns_servers(self) -> list[str]:
        """Resolves active DNS servers."""
        dns = []
        # Method 1: getprop (Android)
        try:
            res = subprocess.run(
                ["getprop"], capture_output=True, text=True, check=False, timeout=2
            )
            for line in res.stdout.splitlines():
                if "dns" in line.lower() and "[" in line and "]" in line:
                    parts = line.split("]: [")
                    if len(parts) >= 2:
                        val = parts[1].strip("] ")
                        if val and "." in val:
                            dns.append(val)
        except Exception:
            pass

        if not dns:
            # Method 2: resolv.conf
            try:
                with open("/etc/resolv.conf", "r") as f:
                    for line in f:
                        if line.startswith("nameserver"):
                            dns.append(line.split()[1])
            except Exception:
                pass
        return list(set(dns))

    def _get_routing_topology(self) -> dict:
        """Parses active default gateway routes to identify true internet-facing transport."""
        topo = {"wifi_active": False, "fabric": "CELLULAR", "interface": "NONE"}
        try:
            res = subprocess.run(
                ["ip", "route", "show"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                lines = res.stdout.splitlines()
                for line in lines:
                    if "default" in line:
                        if "wlan" in line:
                            topo["wifi_active"] = True
                            topo["fabric"] = "WI-FI"
                        elif any(c in line for c in ["rmnet", "ccmni", "rndis", "p2p"]):
                            topo["fabric"] = "CELLULAR"
                        break
        except (subprocess.SubprocessError, OSError):
            pass
        return topo

    def _check_hotspot_status(self) -> bool:
        """Detects active tethering or AP interfaces in the network stack."""
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()
                if "ap0" in output or "rndis" in output:
                    return True
        except (subprocess.SubprocessError, OSError):
            pass
        return False

    def _check_vpn_status(self) -> dict:
        """Scans network interfaces for active VPN or tunnel links and resolves Geo IP."""
        vpn_info = {
            "active": False,
            "ip": "UNKNOWN",
            "country": "UNKNOWN",
            "isp": "UNKNOWN",
            "org": "UNKNOWN",
            "interface": "NONE",
        }
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()
                for iface in ["tun", "wg0", "ppp0"]:
                    if iface in output:
                        vpn_info["active"] = True
                        vpn_info["interface"] = iface.upper()
                        break
        except (subprocess.SubprocessError, OSError):
            pass

        try:
            req = urllib.request.Request(
                "https://ipapi.co/json/",
                headers={"User-Agent": "TDoc-Telemetry-Client/1.2"},
            )
            with urllib.request.urlopen(req, timeout=2.5) as response:
                data = json.loads(response.read().decode())
                vpn_info["ip"] = data.get("ip", "UNKNOWN")
                vpn_info["country"] = data.get("country_name", "UNKNOWN")
                vpn_info["isp"] = data.get("isp", "UNKNOWN")
                vpn_info["org"] = data.get("org", "UNKNOWN")
                if vpn_info["ip"] != "UNKNOWN":
                    vpn_info["active"] = True
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
            try:
                with urllib.request.urlopen("https://ident.me", timeout=1.5) as r:
                    vpn_info["ip"] = r.read().decode("utf-8").strip()
                    vpn_info["active"] = True
            except (urllib.error.URLError, TimeoutError):
                pass

        return vpn_info

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
