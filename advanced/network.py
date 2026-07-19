"""
TDoc Network Subsystem - Dynamic State Mapping
"""

import json
import subprocess
import urllib.request


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
        try:
            with urllib.request.urlopen(url, timeout=2.0) as _:
                pass
            domain = url.replace("https://", "")
            return True, domain
        except Exception:
            continue

    return False, "All mirror nodes timed out"


def run_network_checks() -> dict:
    """Executes network diagnostics inspecting routes, dynamic states, and mirror failovers."""
    topo = get_routing_topology()
    hotspot_active = check_hotspot_status()
    vpn = check_vpn_status()
    mirror_ok, mirror_msg = check_termux_mirrors()

    return {
        "topology": topo,
        "hotspot_active": hotspot_active,
        "vpn": vpn,
        "mirror": {"online": mirror_ok, "details": mirror_msg},
    }
