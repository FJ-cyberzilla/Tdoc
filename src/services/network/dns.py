import re
import subprocess
from typing import Any


class DNSChecker:
    """
    Identifies active DNS servers by querying system properties and utilizing 'dig'.
    """

    def check(self) -> dict[str, Any]:
        """
        Performs DNS detection. First tries 'dig' for actual resolution path,
        falls back to system properties.
        """
        # 1. Try 'dig' to see what server actually resolved the query
        server = self._get_dns_from_dig()
        dns = [server] if server else []

        # 2. Fallback to system properties
        if not dns:
            dns = self._get_dns_from_getprop()

        status = "OK" if dns else "FAILED: No DNS detected"
        return {"servers": list(set(dns)), "status": status}

    def _get_dns_from_dig(self) -> str | None:
        """Uses 'dig' to find the server that actually resolved a request."""
        try:
            # Run dig and parse the 'SERVER:' field
            result = subprocess.run(
                ["dig", "+short", "google.com"],
                capture_output=True,
                text=True,
                check=True,
                timeout=2,
            )
            # Run again to get the server used
            result = subprocess.run(
                ["dig", "google.com"],
                capture_output=True,
                text=True,
                check=True,
                timeout=2,
            )
            match = re.search(r";; SERVER: ([\d\.]+)", result.stdout)
            return match.group(1) if match else None
        except (subprocess.SubprocessError, Exception):
            return None

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
