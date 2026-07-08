"""
TDoc Core System Helpers and Hardware Boundary Interfaces
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.theme import Theme
from rich.status import Status
from constants import ORANGE_THEME, HOME

logger = logging.getLogger(__name__)
custom_theme = Theme(ORANGE_THEME)
console = Console(theme=custom_theme)

def run_pure_command(cmd: List[str], timeout: float = 3.0) -> Tuple[Optional[str], Optional[str]]:
    """Executes system binaries safely with strict isolation."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.stdout.strip(), proc.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as err:
        logger.debug("Command failed execution %s: %s", cmd, err)
        return None, None

def track_activity(message: str):
    """Generates an orange-spectrum command center progress status spinner."""
    return Status(
        f"[text.primary]{message}[/text.primary]",
        spinner="dots",
        spinner_style="#FF9100",
    )

def diagnose_git_overhead() -> Dict[str, Any]:
    """
    Specifically analyzes the Termux home path for git misconfigurations
    that cause terminal lags and telemetry data bloat.
    """
    home_git = Path(HOME) / ".git"
    analysis = {
        "vulnerable": False,
        "reason": "Clear",
        "file_count": 0,
        "remedy": None
    }
    
    if home_git.is_dir():
        analysis["vulnerable"] = True
        analysis["reason"] = "Stray root repository tracking your entire home path!"
        analysis["remedy"] = "Execute: rm -rf ~/.git"
        
        # Count files roughly to gauge potential lag overhead
        stdout, _ = run_pure_command(["git", "-C", HOME, "ls-files"])
        if stdout:
            analysis["file_count"] = len(stdout.splitlines())
            
    return analysis

def check_termux_api() -> bool:
    """Verifies if the required termux-api subsystem binary hooks are responsive."""
    stdout, _ = run_pure_command(["which", "termux-battery-status"])
    return bool(stdout)

def detect_vpn_interfaces() -> bool:
    """Scans physical network interfaces for active tunneling or VPN locks."""
    stdout, _ = run_pure_command(["ip", "route"])
    if stdout:
        return "tun" in stdout or "ppp" in stdout or "wgp" in stdout
    return False
