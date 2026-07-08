"""
TDoc Network Subsystem - Dynamic State Mapping with Yellow/Green Status Indicators
"""

import json
import os
import subprocess
import sys
import time
import urllib.request

# ANSI Color Matrix
ORANGE = "\033[38;5;208m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def spin_progress(message: str, duration: float = 1.0):
    """Renders a smooth fluid terminal spinner animation during network tasks."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {ORANGE}{frames[i % len(frames)]}{RESET}  {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()


def get_routing_topology() -> dict:
    """Parses active default gateway routes to identify true internet-facing transport."""
    topo = {"wifi_active": False, "fabric": "CELLULAR", "interface": "NONE"}
    try:
        res = subprocess.run(
            ["ip", "route", "show"], capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            lines = res.stdout.splitlines()
            for line in lines:
                if "default" in line:
                    if "wlan" in line:
                        topo["wifi_active"] = True
                        topo["fabric"] = "WI-FI"
                    elif any(c in line for c in ["rmnet", "ccmni", "rndis", "p2p"]):
                        topo["fabric"] = "CELLULAR"
                    break
    except Exception:
        pass
    return topo


def check_hotspot_status() -> bool:
    """Detects active tethering or AP interfaces in the network stack."""
    try:
        res = subprocess.run(
            ["ip", "link"], capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            output = res.stdout.lower()
            if "ap0" in output or "rndis" in output:
                return True
    except Exception:
        pass
    return False


def check_vpn_status() -> dict:
    """Scans network interfaces for active VPN or tunnel links and resolves Geo IP."""
    vpn_info = {
        "active": False,
        "ip": "UNKNOWN",
        "country": "UNKNOWN",
        "interface": "NONE",
    }
    try:
        res = subprocess.run(
            ["ip", "link"], capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            output = res.stdout.lower()
            for iface in ["tun", "wg0", "ppp0"]:
                if iface in output:
                    vpn_info["active"] = True
                    vpn_info["interface"] = iface.upper()
                    break
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            "https://ipapi.co/json/",
            headers={"User-Agent": "TDoc-Telemetry-Client/1.2"},
        )
        with urllib.request.urlopen(req, timeout=2.5) as response:
            data = json.loads(response.read().decode())
            vpn_info["ip"] = data.get("ip", "UNKNOWN")
            vpn_info["country"] = data.get("country_name", "UNKNOWN")
            if vpn_info["ip"] != "UNKNOWN":
                vpn_info["active"] = True
    except Exception:
        try:
            with urllib.request.urlopen("https://ident.me", timeout=1.5) as r:
                vpn_info["ip"] = r.read().decode("utf-8").strip()
                vpn_info["active"] = True
        except Exception:
            pass

    return vpn_info


def check_termux_mirrors() -> tuple:
    """Iterates through an array of redundant mirror nodes until a valid link is established."""
    mirrors = [
        "https://packages.termux.dev",
        "https://packages.termux.org",
        "https://mirror.accum.se",
        "https://mirror.mwt.me",
    ]

    for url in mirrors:
        start_t = time.time()
        try:
            urllib.request.urlopen(url, timeout=2.0)
            latency = (time.time() - start_t) * 1000
            domain = url.replace("https://", "")
            return True, f"ONLINE ({domain} - {latency:.1f}ms)"
        except Exception:
            continue

    return False, "UNREACHABLE (All mirror nodes timed out)"


def run_network_checks():
    """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
    print(f"\n{ORANGE}📡 --- [ TOPOLOGY & SMART ROUTING DIAGNOSTICS ] ---{RESET}")

    spin_progress("Inspecting kernel routing tables...", 0.6)
    topo = get_routing_topology()
    hotspot_active = check_hotspot_status()

    # Conditional Styling for Wi-Fi State
    if topo["wifi_active"]:
        wifi_symbol = f"{GREEN}✓{RESET}"
        wifi_status = f"{GREEN}ACTIVE / CONNECTED{RESET}"
    else:
        wifi_symbol = f"{CYAN}▪{RESET}"
        wifi_status = f"{YELLOW}INACTIVE / UNUSED{RESET}"
    print(f"  {wifi_symbol} Wi-Fi Interface State   : {wifi_status}")
    print(f"  {CYAN}▪{RESET} Active Routing Fabric   : {GREEN}{topo['fabric']}{RESET}")

    # Conditional Styling for Hotspot State
    if hotspot_active:
        hotspot_symbol = f"{GREEN}✓{RESET}"
        hotspot_status = f"{GREEN}ACTIVE{RESET}"
    else:
        hotspot_symbol = f"{CYAN}▪{RESET}"
        hotspot_status = f"{YELLOW}INACTIVE{RESET}"
    print(f"  {hotspot_symbol} Hotspot Tethering Core  : {hotspot_status}")

    spin_progress("Interrogating VPN and geolocation endpoints...", 1.0)
    vpn = check_vpn_status()
    if vpn["active"]:
        if_name = vpn["interface"] if vpn["interface"] != "NONE" else "TUNNEL"
        print(
            f"  {CYAN}▪{RESET} VPN Interception Layer  : {GREEN}ONLINE ({if_name}){RESET}"
        )
        print(f"  {GREEN}✓{RESET} External Telemetry IP   : {BOLD}{vpn['ip']}{RESET}")
        print(
            f"  {GREEN}✓{RESET} Geolocation Origin      : {BOLD}{vpn['country']}{RESET}"
        )
    else:
        print(f"  {CYAN}▪{RESET} VPN Interception Layer  : {RED}OFFLINE{RESET}")
        print(f"  {RED}x{RESET} External Telemetry IP   : {DIM}MASKED / UNKNOWN{RESET}")

    spin_progress("Probing backup mirror nodes rotation array...", 0.8)
    mirror_ok, mirror_msg = check_termux_mirrors()
    if mirror_ok:
        print(f"  {GREEN}✓{RESET} Termux Repository Mirror: {GREEN}{mirror_msg}{RESET}")
    else:
        print(f"  {RED}❌{RESET} Termux Repository Mirror: {RED}{mirror_msg}{RESET}")
