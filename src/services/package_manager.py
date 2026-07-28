"""
TDoc Package Manager - Installed Package Inventory
"""

import subprocess

from src.interfaces import DiagnosticService


class PackageManagerService(DiagnosticService):
    """Service to inventory installed packages using dpkg."""

    def run(self) -> dict:
        """Retrieves a list of all installed packages."""
        return {"packages": self._get_package_list()}

    def search(self, query: str) -> dict:
        """Retrieves packages matching the search query."""
        all_pkgs = self._get_package_list()
        filtered = [pkg for pkg in all_pkgs if query.lower() in pkg.lower()]
        return {"packages": filtered}

    def _get_package_list(self) -> list[str]:
        """Uses dpkg-query to fetch package names efficiently."""
        try:
            cmd = ["dpkg-query", "-l"]
            # Pipeline: dpkg-query -l | awk '{print $2}' | tail -n +6
            # tail -n +6 skips the header lines in dpkg output
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)

            pkgs = []
            lines = res.stdout.splitlines()
            # Skip the first 5 lines (header)
            for line in lines[5:]:
                parts = line.split()
                if len(parts) >= 2:
                    pkgs.append(parts[1])
            return pkgs
        except (subprocess.SubprocessError, OSError, IndexError):
            return []
