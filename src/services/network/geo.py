import json
import urllib.request
from typing import Any


class IPGeolocationService:
    """
    Provides IP-based geolocation by querying external services.

    It tries multiple services in order to ensure reliability (failover pattern).
    """

    SERVICES: list[dict[str, Any]] = [
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
        """
        Retrieves geolocation details for the current public IP.

        Args:
            timeout: Maximum time to wait for each service request.

        Returns:
            dict: Geolocation details (ip, country, isp, org).
        """
        for service in self.SERVICES:
            try:
                data = self._fetch(service["url"], timeout)
                details = self._extract(data, service["mapping"])
                if details.get("ip"):
                    return details
            except Exception:  # noqa: S112
                # Silencing exception to try the next geolocation service in the list
                # This provides resilience against service downtime.
                continue

        # Final fallback if all external API services fail
        return {
            "ip": self._get_public_ip(),
            "country": None,
            "isp": None,
            "org": None,
        }

    def _fetch(self, url: str, timeout: float) -> dict:
        """Performs an HTTP GET request and returns parsed JSON."""
        req = urllib.request.Request(url, headers={"User-Agent": "TDoc-Telemetry-Client/1.2"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())

    def _extract(self, data: dict, mapping: dict) -> dict[str, str | None]:
        """Maps service-specific JSON keys to an internal unified format."""
        result: dict[str, str | None] = {}
        for key, fields in mapping.items():
            for field in fields:
                if data.get(field):
                    result[key] = data[field]
                    break
            else:
                result[key] = None
        return result

    def _get_public_ip(self) -> str | None:
        """Fallback method to get ONLY the public IP via ident.me."""
        try:
            with urllib.request.urlopen("https://ident.me", timeout=1.5) as r:
                return r.read().decode("utf-8").strip()
        except Exception:
            return None
