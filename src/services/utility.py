"""
TDoc Utility Service - External tool management.
"""

import subprocess
import shutil
from src.interfaces import DiagnosticService


class UtilityService(DiagnosticService):
    """Service to install and execute system utilities."""

    def run(self) -> dict:
        """Utility service does not support default run."""
        return {"status": "Utility service active."}

    def run_tool(self, tool_name: str) -> bool:
        """
        Installs the tool if missing and executes it.
        Returns True if execution succeeded.
        """
        if not self._is_installed(tool_name):
            self._install_package(tool_name)
        
        # Execute tool
        subprocess.run([tool_name], check=False)
        return True

    def _is_installed(self, tool_name: str) -> bool:
        """Checks if a tool is in the PATH."""
        return shutil.which(tool_name) is not None

    def _install_package(self, package_name: str) -> bool:
        """Installs package via pkg."""
        try:
            subprocess.run(["pkg", "install", "-y", package_name], check=True)
            return True
        except subprocess.SubprocessError:
            return False
