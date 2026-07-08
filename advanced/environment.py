"""
TDoc Command Center - Termux Platform Infrastructure & Environment Auditing
"""

import os
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.theme import Theme
from constants import ORANGE_THEME, HOME, PREFIX
from helper import run_pure_command

console = Console(theme=Theme(ORANGE_THEME))

def verify_storage_setup() -> bool:
    """Validates that termux-setup-storage has run and symlinks are active."""
    storage_path = Path(HOME) / "storage"
    if not storage_path.is_dir():
        console.print("  [status.critical]✗ Shared Storage Symlink Absent[/status.critical]")
        console.print("    [text.muted]Remedy: Run 'termux-setup-storage' to grant access.[/text.muted]")
        return False
        
    # Check if links point outward to shared memory structures
    is_linked = any(p.is_symlink() for p in storage_path.iterdir() if p.is_symlink())
    if is_linked:
        console.print("  [status.optimal]✓ Shared Storage Mount: ACCESSIBLE & SYMLINKED[/status.optimal]")
        return True
    
    console.print("  [status.warning]⚠️ Storage Warning:[/status.warning] Directory exists but links are broken.")
    return False

def verify_termux_api_subsystem() -> Dict[str, Any]:
    """Tests communication with the underlying Termux:API Android wrapper service."""
    status = {"installed": False, "responsive": False}
    if Path(PREFIX).joinpath("bin", "termux-api-start").exists() or shutil.which("termux-battery-status"):
        status["installed"] = True
        
        # Test responsiveness with a tight timeout to avoid hanging the HUD
        stdout, _ = run_pure_command(["termux-api-start"], timeout=1.0)
        stdout_bat, _ = run_pure_command(["termux-battery-status"], timeout=1.5)
        if stdout_bat:
            status["responsive"] = True
            console.print("  [status.optimal]✓ Termux:API Ecosystem: CONNECTED & RESPONSIVE[/status.optimal]")
        else:
            console.print("  [status.warning]⚠️ Termux:API Bridge Lagging:[/status.warning] Binaries exist but service timed out.")
    else:
        console.print("  [status.warning]▪ Termux:API Subsystem: NOT DEPLOYED[/status.warning]")
    return status

def check_boot_scripts() -> None:
    """Audits Termux:Boot structural persistence rules and scripts."""
    boot_dir = Path(HOME) / ".termux" / "boot"
    if not boot_dir.is_dir():
        console.print("  [text.muted]▪ Termux:Boot Startup Nodes: Inactive (Directory absent)[/text.muted]")
        return

    scripts = [s for s in boot_dir.iterdir() if s.is_file()]
    if scripts:
        console.print(f"  [status.optimal]✓[/status.optimal] Termux:Boot Persistence: {len(scripts)} Active Boot Scripts Found")
        for s in scripts:
            # Check for executable bit safety
            is_exec = os.access(s, os.X_OK)
            status_str = "[status.optimal]EXEC[/status.optimal]" if is_exec else "[status.critical]NON-EXEC[/status.critical]"
            console.print(f"    ⨠ {s.name} ({status_str})")
    else:
        console.print("  [text.muted]▪ Termux:Boot Persistence: Configured directory is empty.[/text.muted]")

def validate_locale_and_encoding() -> None:
    """Validates env encoding limits to prevent text clipping in the rich HUD."""
    lang = os.environ.get("LANG", "Unknown")
    is_utf8 = "utf-8" in lang.lower() or "utf8" in lang.lower()
    
    if is_utf8:
        console.print(f"  [status.optimal]✓[/status.optimal] Terminal Environment Encoding: [text.primary]{lang}[/text.primary] (UTF-8 Compliant)")
    else:
        console.print(f"  [status.critical]✗ Non-UTF8 Locale Detected ({lang})[/status.critical]")
        console.print("    [text.muted]Fix: Export LANG=en_US.UTF-8 inside your shell profiles.[/text.muted]")
