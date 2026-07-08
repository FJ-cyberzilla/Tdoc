"""
TDoc Command Center - Advanced Network Engine
"""

import json
import logging
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Any

import requests
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.theme import Theme

from constants import CHECK_SITES, DNS_PROVIDERS, SCAN_PORTS, ORANGE_THEME
import helper

logger = logging.getLogger(__name__)
console = Console(theme=Theme(ORANGE_THEME))

def scan_ports_with_progress() -> Dict[int, str]:
    """Scans ports concurrently with an interactive orange spectrum progress bar."""
    results = {}
    
    with Progress(
        SpinnerColumn(spinner_name="dots", style="#FF9100"),
        TextColumn("[text.primary]{task.description}[/text.primary]"),
        BarColumn(bar_width=30, style="#FFD180", complete_style="#FF6D00"),
        TextColumn("[text.muted]{task.completed}/{task.total}[/text.muted]"),
        console=console,
    ) as progress:
        
        task = progress.add_task("Auditing local port sockets...", total=len(SCAN_PORTS))
        
        def _check_single_port(port: int) -> Tuple[int, str]:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.4):
                    return port, "OPEN"
            except (socket.timeout, ConnectionRefusedError, OSError):
                return port, "CLOSED"
            finally:
                progress.advance(task)

            return port, "UNKNOWN"

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(_check_single_port, p) for p in SCAN_PORTS]
            for future in as_completed(futures):
                p, status = future.result()
                results[p] = status

    # Print a clean, stylized dashboard panel of findings
    open_ports = [port for port, status in results.items() if status == "OPEN"]
    if open_ports:
        console.print(Panel(
            f"[status.warning]⚠️ Exposed Ports Detected:[/status.warning] {open_ports}\n"
            f"[text.muted]Verify if these services (like SSH or development servers) "
            f"should be accessible inside Termux.[/text.muted]",
            border_style="#FF9100",
            title="[banner]Port Security Matrix[/banner]"
        ))
    else:
        console.print("[status.optimal]✓ Port Security Check passed. No leaks found.[/status.optimal]")
        
    return results

def run_advanced_ping() -> List[Dict[str, Any]]:
    """Validates global connectivity, watches for VPN drag, and offers direct fixes."""
    telemetry = []
    vpn_active = helper.detect_vpn_interfaces()
    
    console.print("\n[text.primary]📡 Running VPN-Aware Latency Calculations...[/text.primary]")
    
    for site in CHECK_SITES:
        clean_host = site["url"].split("//")[-1].split("/")[0]
        start_time = time.monotonic()
        
        # Real low-level socket verification to avoid slow ping binary lockups
        try:
            socket.setdefaulttimeout(1.5)
            socket.gethostbyname(clean_host)
            latency = (time.monotonic() - start_time) * 1000
            status = "OPTIMAL"
            color = "status.optimal"
            troubleshoot = None
        except socket.error:
            latency = -1
            status = "BLOCKED"
            color = "status.critical"
            troubleshoot = "Check Termux network access, or toggle your current VPN/Firewall."

        # Analyze anomalies
        if latency > 250 and vpn_active and site["type"] == "local":
            status = "WARNING"
            color = "status.warning"
            troubleshoot = "High latency detected. Your current VPN interface might be misconfigured."

        telemetry.append({
            "name": site["name"],
            "latency_ms": latency,
            "status": status,
            "troubleshoot": troubleshoot
        })
        
        latency_str = f"{latency:.1f}ms" if latency >= 0 else "TIMEOUT"
        console.print(f"  [{color}]▪[/{color}] [text.primary]{site['name']:<18}[/text.primary] → "
                      f"[{color}]{latency_str:<10}[/{color}] ({status})")
        if troubleshoot:
            console.print(f"    [text.muted]💡 Remedy: {troubleshoot}[/text.muted]")

    return telemetry
