import json
import subprocess
import urllib.request
from typing import Any, Protocol


class IPGeolocationService:
    SERVICES = [
        {
            "url": "http://ip-api.com/json/",
            "mapping": {
                "ip": ["query", "ip"],
                "country": ["country", "country_name"],
                "isp": ["isp"],
                "org": ["org"],
            },
        },
        {
            "url": "https://ipapi.co/json/",
            "mapping": {
                "ip": ["query", "ip"],
                "country": ["country", "country_name"],
                "isp": ["isp"],
                "org": ["org"],
            },
        },
    ]

    def get_details(self, timeout: float = 2.5) -> dict[str, str | None]:
        for service in self.SERVICES:
            try:
                data = self._fetch(service["url"], timeout)
                details = self._extract(data, service["mapping"])
                if details.get("ip"):
                    return details
            except Exception:  # noqa: S112
                # Silencing exception to try the next geolocation service in the list
                continue

        # Final fallback
        return {
            "ip": self._get_public_ip(),
            "country": None,
            "isp": None,
            "org": None,
        }

    def _fetch(self, url: str, timeout: float) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "TDoc-Telemetry-Client/1.2"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())

    def _extract(self, data: dict, mapping: dict) -> dict[str, str | None]:
        result = {}
        for key, fields in mapping.items():
            for field in fields:
                if data.get(field):
                    result[key] = data[field]
                    break
            else:
                result[key] = None
        return result

    def _get_public_ip(self) -> str | None:
        try:
            with urllib.request.urlopen("https://ident.me", timeout=1.5) as r:
                return r.read().decode("utf-8").strip()
        except Exception:
            return None


class NetworkChecker(Protocol):
    def check(self) -> Any:
        """Performs a network diagnostic check."""
        ...


class DNSChecker:
    def check(self) -> dict[str, Any]:
        """Performs DNS detection with diagnostic reporting."""
        dns = []
        status = "OK"

        # 1. Advanced getprop lookup
        dns = self._get_dns_from_getprop()
        if not dns:
            # 2. Fallback to /etc/resolv.conf
            dns = self._get_dns_from_resolv_conf()
            if not dns:
                status = "FAILED: No DNS servers detected via getprop or /etc/resolv.conf"

        return {"servers": list(set(dns)), "status": status}

    def _get_dns_from_getprop(self) -> list[str]:
        dns = []
        # Target known Android property keys
        keys = ["net.dns1", "net.dns2", "net.dns3", "net.dns4"]
        for key in keys:
            try:
                res = subprocess.run(
                    ["getprop", key], capture_output=True, text=True, check=False, timeout=1
                )
                if res.returncode == 0 and res.stdout.strip():
                    dns.append(res.stdout.strip())
            except Exception:  # noqa: S112
                continue
        return dns

    def _get_dns_from_resolv_conf(self) -> list[str]:
        dns = []
        try:
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        parts = line.split()
                        if len(parts) > 1:
                            dns.append(parts[1])
        except PermissionError:
            pass  # We can't fix permissions, but we know it's a reason for failure
        except Exception:
            pass
        return dns


class RoutingTopologyChecker:
    def check(self) -> dict[str, Any]:
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
        topo = {"wifi_active": False, "fabric": "CELLULAR", "interface": "NONE"}
        for line in output.splitlines():
            if "default" in line:
                self._update_topology_from_line(topo, line)
                break
        return topo

    def _update_topology_from_line(self, topo: dict[str, Any], line: str):
        if "wlan" in line:
            topo["wifi_active"] = True
            topo["fabric"] = "WI-FI"
        elif any(c in line for c in ["rmnet", "ccmni", "rndis", "p2p"]):
            topo["fabric"] = "CELLULAR"


class VPNStatusChecker:
    def __init__(self):
        self.geo_service = IPGeolocationService()

    def check(self) -> dict[str, Any]:
        vpn_info = {
            "active": False,
            "ip": "UNKNOWN",
            "country": "UNKNOWN",
            "isp": "UNKNOWN",
            "org": "UNKNOWN",
            "interface": "NONE",
        }
        vpn_info["active"], vpn_info["interface"] = self._check_vpn_interfaces()

        details = self.geo_service.get_details()
        vpn_info.update(details)

        if vpn_info["ip"] != "UNKNOWN":
            vpn_info["active"] = True

        return vpn_info

    def _check_vpn_interfaces(self) -> tuple[bool, str]:
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


class HotspotChecker:
    def check(self) -> bool:
        try:
            res = subprocess.run(
                ["ip", "link"], capture_output=True, text=True, check=False, timeout=2
            )
            if res.returncode == 0:
                output = res.stdout.lower()
                return "ap0" in output or "rndis" in output
        except (subprocess.SubprocessError, OSError):
            pass
        return False
