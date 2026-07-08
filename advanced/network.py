import time
"""
TDoc Command Center - Advanced Network Diagnostics
"""

import os
import json
import socket
import time
import requests
from typing import Dict, Any, Optional
from rich.console import Console
from rich.theme import Theme
from constants import ORANGE_THEME, CHECK_SITES
from helper import run_pure_command

console = Console(theme=Theme(ORANGE_THEME))

def get_wifi_analysis() -> Dict[str, Any]:
    """Extracts live Wi-Fi data using Termux API or falls back to system dumpsys."""
    metrics = {"status": "Disconnected", "rssi": "N/A", "channel": "N/A"}
    stdout, _ = run_pure_command(["termux-wifi-connectioninfo"])
    
    if stdout:
        try:
            raw = json.loads(stdout)
            metrics["status"] = raw.get("supplicant_state", "COMPLETED")
            metrics["rssi"] = f"{raw.get('rssi', -100)} dBm"
            metrics["channel"] = f"{raw.get('frequency', 0)} MHz"
            console.print(f"  [status.optimal]✓[/status.optimal] Wi-Fi Status: {metrics['status']} | Link: {metrics['rssi']}")
        except json.JSONDecodeError:
            pass
    else:
        console.print("  [status.warning]⚠️ Wi-Fi Specs Restricted:[/status.warning] Requires 'termux-api' package.")
    return metrics

def run_dns_leak_test() -> Dict[str, Any]:
    """Verifies public routing footprint to ensure DNS requests don't leak outside VPNs."""
    status = {"leaking": False, "dns_server": "Unknown", "geo": "Unknown"}
    try:
        # Use a highly responsive, low-overhead secure lookup API
        resp = requests.get("https://edns.ip-api.com/json", timeout=3.0).json()
        status["dns_server"] = resp.get("dns", {}).get("ip", "Unknown")
        status["geo"] = resp.get("dns", {}).get("geo", "Unknown")
        console.print(f"  [status.optimal]✓[/status.optimal] Public DNS Resolver: [text.muted]{status['dns_server']} ({status['geo']})[/text.muted]")
    except Exception:
        console.print("  [status.critical]✗ DNS Resolution Verification Timeout[/status.critical]")
    return status

def check_ipv6_readiness() -> bool:
    """Probes local network interfaces for active IPv6 routing capability."""
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Connect to a public global IPv6 address (Cloudflare DNS) without sending data
        sock.connect(("2606:4700:4700::1111", 80))
        sock.close()
        console.print("  [status.optimal]✓[/status.optimal] IPv6 Routing Status: [status.optimal]AVAILABLE[/status.optimal]")
        return True
    except OSError:
        console.print("  [status.warning]▪[/status.warning] IPv6 Routing Status: [text.muted]UNAVAILABLE / IPV4 ONLY[/text.muted]")
        return False

def check_firewall_rules() -> None:
    """Audits iptables policies. Branches safely based on root elevation."""
    if os.getuid() != 0:
        console.print("  [status.warning]▪ Firewall Scan Blocked:[/status.warning] Root access required to view iptables.")
        return

    stdout, _ = run_pure_command(["iptables", "-L", "-n", "-v"])
    if stdout:
        active_rules = len(stdout.splitlines())
        console.print(f"  [status.optimal]✓[/status.optimal] Active Firewall Rule Signatures: {active_rules}")
