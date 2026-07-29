import time
import urllib.request
from typing import Any

from src.exceptions import NetworkError


class NetworkSpeedChecker:
    """
    Measures download speed by timing the fetch of a small asset or mirror endpoint.
    """

    def check(self) -> dict[str, Any]:
        """
        Executes a basic latency and download speed check.

        Returns:
            dict: Latency and speed statistics.
        """
        url = "https://packages.termux.dev"
        start_time = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TDoc-Telemetry-Client/1.2"})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                content = response.read(1024 * 10)  # read up to 10KB
                size_kb = len(content) / 1024
            duration = time.time() - start_time
            speed_kb_s = size_kb / duration if duration > 0 else 0.0
            return {
                "status": "OK",
                "latency_ms": duration * 1000,
                "speed_kb_s": speed_kb_s,
            }
        except Exception as e:
            raise NetworkError(f"Network speed check failed: {e}", context={"url": url}) from e
