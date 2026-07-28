"""
TDoc Command Center - Advanced Network Engine
"""

import logging
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from src.constants import CHECK_SITES, SCAN_PORTS
from src.utils import helper

logger = logging.getLogger(__name__)


class PortScanner:
    """Service to scan ports concurrently."""

    def run(self) -> dict[int, str]:
        """Scans ports concurrently with an interactive orange spectrum progress bar."""
        results = {}

        with Progress(
            SpinnerColumn(spinner_name="dots", style="#FF9100"),
            TextColumn("[text.primary]{task.description}[/text.primary]"),
            BarColumn(bar_width=30, style="#FFD180", complete_style="#FF6D00"),
            TextColumn("[text.muted]{task.completed}/{task.total}[/text.muted]"),
        ) as progress:
            task = progress.add_task("Auditing local port sockets...", total=len(SCAN_PORTS))

            def _check_single_port(port: int) -> tuple[int, str]:
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=0.4):
                        return port, "OPEN"
                except (TimeoutError, ConnectionRefusedError, OSError):
                    return port, "CLOSED"
                finally:
                    progress.advance(task)

            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(_check_single_port, p) for p in SCAN_PORTS]
                for future in as_completed(futures):
                    p, status = future.result()
                    results[p] = status

        return results


class ConnectivityAnalyzer:
    """Service to validate global connectivity."""

    def run(self) -> list[dict[str, Any]]:
        """Validates global connectivity, watches for VPN drag, and offers direct fixes."""
        telemetry = []
        vpn_active = helper.detect_vpn_interfaces()

        for site in CHECK_SITES:
            latency, status, troubleshoot = self._verify_site_connectivity(site["url"])

            # Analyze anomalies
            if status == "OPTIMAL" and latency > 250 and vpn_active and site["type"] == "local":
                status = "WARNING"
                troubleshoot = (
                    "High latency detected. Your current VPN interface might be misconfigured."
                )

            telemetry.append(
                {
                    "name": site["name"],
                    "latency_ms": latency,
                    "status": status,
                    "troubleshoot": troubleshoot,
                }
            )

        return telemetry

    def _verify_site_connectivity(self, url: str) -> tuple[float, str, str | None]:
        """Performs low-level socket verification."""
        clean_host = url.split("//")[-1].split("/")[0]
        start_time = time.monotonic()

        try:
            socket.setdefaulttimeout(1.5)
            socket.gethostbyname(clean_host)
            latency = (time.monotonic() - start_time) * 1000
            return latency, "OPTIMAL", None
        except OSError:
            return (
                -1.0,
                "BLOCKED",
                "Check Termux network access, or toggle your current VPN/Firewall.",
            )
