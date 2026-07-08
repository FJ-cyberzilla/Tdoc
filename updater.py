"""
TDoc Command Center - Auto-Update and Integrity Synchronization Engine
"""

import logging
from typing import Tuple
import helper
from rich.console import Console
from rich.theme import Theme
from constants import ORANGE_THEME

logger = logging.getLogger(__name__)
console = Console(theme=Theme(ORANGE_THEME))

def check_for_updates() -> Tuple[bool, str]:
    """
    Queries the underlying git tracking stream safely.
    Returns (update_available, action_message)
    """
    # Silently check if git exists in the path
    stdout, _ = helper.run_pure_command(["git", "rev-parse", "--is-inside-work-tree"])
    if not stdout:
        return False, "Not tracked within an active Git environment."

    console.print("[text.primary]🔄 Checking upstream servers for TDoc code updates...[/text.primary]")
    
    # Fetch data without mutating local index
    helper.run_pure_command(["git", "fetch", "origin"], timeout=4.0)
    
    local_sha, _ = helper.run_pure_command(["git", "rev-parse", "HEAD"])
    remote_sha, _ = helper.run_pure_command(["git", "rev-parse", "@{u}"])
    
    if not local_sha or not remote_sha:
        return False, "Unable to verify signature synchronizations (Offline)."
        
    if local_sha != remote_sha:
        return True, "An optimization update is waiting on the server."
        
    return False, "TDoc is running on the absolute latest codebase specification."

def perform_upgrade() -> bool:
    """Executes a hard pull to sync code assets directly on user approval."""
    console.print("[status.warning]🗲 Upgrading TDoc systems core...[/status.warning]")
    stdout, stderr = helper.run_pure_command(["git", "pull", "--rebase"])
    if stdout and "Already up to date" not in stdout:
        console.print("[status.optimal]✅ Upgrade completed successfully! Restarting modules...[/status.optimal]")
        return True
    return False
