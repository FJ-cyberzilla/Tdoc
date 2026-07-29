import os
from typing import Any


class ProxyChecker:
    """
    Detects active proxy configurations via environment variables.
    """

    def check(self) -> dict[str, Any]:
        """
        Checks for proxy environment variables and settings.

        Returns:
            dict: Proxy status and detected proxy addresses.
        """
        proxies: dict[str, str] = {}
        for var in [
            "http_proxy",
            "https_proxy",
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "all_proxy",
            "ALL_PROXY",
        ]:
            if var in os.environ:
                proxies[var] = os.environ[var]

        active = len(proxies) > 0
        return {
            "active": active,
            "proxies": proxies,
        }
