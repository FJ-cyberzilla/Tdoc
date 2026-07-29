"""
TDoc Command Center - Advanced Network Diagnostic Engine.

This module provides the core high-performance diagnostic services for TDoc,
specifically focusing on concurrent network port scanning and global connectivity
latency analysis.

Services:
    - PortScanner: Uses a ThreadPoolExecutor to perform concurrent TCP socket
      scans against predefined port lists. Features a rich terminal progress bar.
    - ConnectivityAnalyzer: Validates network health by checking latency against
      a set of critical endpoints and detecting anomalies (e.g., VPN drag).

Example usage:
    scanner = PortScanner()
    open_ports = scanner.run()

    analyzer = ConnectivityAnalyzer()
    network_telemetry = analyzer.run()
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
    """
    Service to perform concurrent local network port scans.

    Utilizes a ThreadPoolExecutor to efficiently check multiple ports simultaneously
    with a capped concurrency limit.
    """

    def run(self) -> dict[int, str]:
        """
        Scans predefined ports concurrently and returns their status.

        The method features an interactive orange-spectrum progress bar provided
        by the `rich` library.

        Returns:
            dict[int, str]: A dictionary mapping port numbers to their status ('OPEN' or 'CLOSED').
        """
        results = {}

        with Progress(
            SpinnerColumn(spinner_name="dots", style="#FF9100"),
            TextColumn("[text.primary]{task.description}[/text.primary]"),
            BarColumn(bar_width=30, style="#FFD180", complete_style="#FF6D00"),
            TextColumn("[text.muted]{task.completed}/{task.total}[/text.muted]"),
        ) as progress:
            task = progress.add_task("Auditing local port sockets...", total=len(SCAN_PORTS))

            def _check_single_port(port: int) -> tuple[int, str]:
                """Checks availability of a single TCP port."""
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=0.4):
                        return port, "OPEN"
                except (TimeoutError, ConnectionRefusedError, OSError):
                    return port, "CLOSED"
                finally:
                    progress.advance(task)

            # Cap concurrency to 8 threads to avoid resource exhaustion
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(_check_single_port, p) for p in SCAN_PORTS]
                for future in as_completed(futures):
                    p, status = future.result()
                    results[p] = status

        return results


class ConnectivityAnalyzer:
    """
    Service to validate global connectivity and network health.

    Performs latency checks against critical endpoints and performs basic
    anomaly detection (e.g., identifying VPN-related latency spikes).
    """

    def run(self) -> list[dict[str, Any]]:
        """
        Validates global connectivity.

        Checks latency, status, and provides troubleshooting guidance for
        predefined endpoints.

        Returns:
            list[dict[str, Any]]: A list of dictionaries, each containing
            site 'name', 'latency_ms', 'status', and 'troubleshoot' advice.
        """
        telemetry = []
        vpn_active = helper.detect_vpn_interfaces()

        for site in CHECK_SITES:
            latency, status, troubleshoot = self._verify_site_connectivity(site["url"])

            # Apply anomaly detection
            status, troubleshoot = self._apply_anomaly_detection(
                site, latency, status, troubleshoot, vpn_active
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

    def _apply_anomaly_detection(
        self,
        site: dict[str, Any],
        latency: float,
        status: str,
        troubleshoot: str | None,
        vpn_active: bool,
    ) -> tuple[str, str | None]:
        """
        Adjusts status and troubleshooting based on network context.
        """
        if status == "OPTIMAL" and latency > 250 and vpn_active and site.get("type") == "local":
            return (
                "WARNING",
                "High latency detected. Your current VPN interface might be misconfigured.",
            )
        return status, troubleshoot

    def _verify_site_connectivity(self, url: str) -> tuple[float, str, str | None]:
        """
        Performs low-level socket-based latency verification.

        Args:
            url (str): The URL/host string to check.

        Returns:
            tuple[float, str, str | None]: (latency_in_ms, status_label, error_message).
        """
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
