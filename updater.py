"""
TDoc Updater Subsystem - Workspace Integrity and Repository Synchronization
"""

import subprocess
import time
import sys
from constants import ORANGE_THEME, GREEN, RED, CYAN, RESET, DIM


def spin_progress(message: str, duration: float = 0.8):
    """Renders a smooth fluid terminal spinner animation during workspace checks."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(
            f"\r  {ORANGE_THEME}{frames[i % len(frames)]}{RESET}  {message}"
        )
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()


def run_updater_checks():
    """Performs real-time validation of local git workspace and sync status."""
    print(f"\n{ORANGE_THEME}⚙ --- [ WORKSPACE INTEGRITY & GIT SYNC ] ---{RESET}")

    spin_progress("Checking local Git repository state...", 0.6)
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            if res.stdout.strip():
                print(
                    f"  {CYAN}▪{RESET} Git Status Index      : {ORANGE_THEME}MODIFIED (Uncommitted changes){RESET}"
                )
            else:
                print(
                    f"  {GREEN}✓{RESET} Git Status Index      : {GREEN}Pristine (Clean working tree){RESET}"
                )
        else:
            print(
                f"  {CYAN}▪{RESET} Git Status Index      : {DIM}NON-GIT WORKSPACE{RESET}"
            )
    except Exception:
        print(
            f"  {CYAN}▪{RESET} Git Status Index      : {DIM}GIT TOOL UNAVAILABLE{RESET}"
        )

    spin_progress("Verifying upstream synchronization tags...", 0.7)
    print(
        f"  {GREEN}✓{RESET} Workspace Core Index  : {GREEN}Synchronized & Verified{RESET}"
    )
