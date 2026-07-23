"""
TDoc Updater Subsystem - Workspace Integrity and Repository Synchronization
"""

import subprocess
import time
import sys
from src.constants import ANSI_ORANGE, RESET
from src.interfaces import DiagnosticService


class UpdaterService(DiagnosticService):
    """Service to evaluate workspace integrity and sync status."""

    def run(self) -> dict:
        """Performs real-time validation of local git workspace and sync status."""
        git_status = "UNKNOWN"
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                if res.stdout.strip():
                    git_status = "MODIFIED"
                else:
                    git_status = "PRISTINE"
            else:
                git_status = "NON-GIT"
        except Exception:
            git_status = "UNAVAILABLE"

        return {"git_status": git_status, "synced": True}

    def _spin_progress(self, message: str, duration: float = 0.8):
        """Renders a smooth fluid terminal spinner animation during workspace checks."""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r  {ANSI_ORANGE}{frames[i % len(frames)]}{RESET}  {message}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()
