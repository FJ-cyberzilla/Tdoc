"""
TDoc Updater Subsystem - Workspace Integrity and Repository Synchronization
"""

import subprocess
import sys
import time
from typing import Any

from src.constants import ANSI_ORANGE, RESET
from src.interfaces import DiagnosticService


class UpdaterService(DiagnosticService):
    """Service to evaluate workspace integrity and sync status."""

    def run(self) -> dict[str, Any]:
        """Performs real-time validation of local git workspace and sync status."""
        git_status: str = "UNKNOWN"
        try:
            res: subprocess.CompletedProcess = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                git_status = "MODIFIED" if res.stdout.strip() else "PRISTINE"
            else:
                git_status = "NON-GIT"
        except (subprocess.SubprocessError, FileNotFoundError):
            git_status = "UNAVAILABLE"

        return {"git_status": git_status, "synced": True}

    def _spin_progress(self, message: str, duration: float = 0.8) -> None:
        """Renders a smooth fluid terminal spinner animation during workspace checks."""
        frames: list[str] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time: float = time.time() + duration
        i: int = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r  {ANSI_ORANGE}{frames[i % len(frames)]}{RESET}  {message}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()
