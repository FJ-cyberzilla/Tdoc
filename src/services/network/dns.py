import os
import subprocess
from typing import Any


class DNSChecker:
    """
    Identifies active DNS servers by querying system properties and files.
    """

    def check(self) -> dict[str, Any]:
        """
        Performs DNS detection with diagnostic reporting.

        Returns:
            dict: List of 'servers' and a 'status' message.
        """
        dns = self._get_dns_from_getprop()
        if not dns:
            dns = self._get_dns_from_resolv_conf()

        status = "OK" if dns else "FAILED: No DNS servers detected via getprop or /etc/resolv.conf"
        return {"servers": list(set(dns)), "status": status}

    def _get_dns_from_getprop(self) -> list[str]:
        """Queries Android system properties for DNS settings."""
        dns = []
        for i in range(1, 5):
            key = f"net.dns{i}"
            server = self._query_property(key)
            if server:
                dns.append(server)
        return dns

    def _query_property(self, key: str) -> str | None:
        try:
            res = subprocess.run(
                ["getprop", key], capture_output=True, text=True, check=False, timeout=1
            )
            return res.stdout.strip() if res.returncode == 0 and res.stdout.strip() else None
        except Exception:
            return None

    def _get_dns_from_resolv_conf(self) -> list[str]:
        """Reads DNS servers from /etc/resolv.conf."""
        if not os.path.exists("/etc/resolv.conf"):
            return []

        try:
            with open("/etc/resolv.conf") as f:
                return self._parse_resolv_conf(f)
        except (PermissionError, Exception):
            return []

    def _parse_resolv_conf(self, file_object: Any) -> list[str]:
        dns = []
        for line in file_object:
            if line.startswith("nameserver"):
                parts = line.split()
                if len(parts) > 1:
                    dns.append(parts[1])
        return dns
