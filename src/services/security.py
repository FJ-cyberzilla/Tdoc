"""
TDoc Security Subsystem – Hardened Privilege Audit
"""

from src.interfaces import DiagnosticService
from src.services.security_checkers import (
    LDPreloadChecker,
    RootPresenceChecker,
    SELinuxStatusChecker,
    SUIDBinaryChecker,
)


class SecurityService(DiagnosticService):
    """Service to evaluate system security and privilege status."""

    def __init__(self):
        self._checkers = {
            "root_presence": RootPresenceChecker(),
            "selinux": SELinuxStatusChecker(),
            "ld_preload": LDPreloadChecker(),
            "termux_suid": SUIDBinaryChecker(),
        }

    def run(self) -> dict:
        """Executes host privilege security audit with real system inspection."""
        results = {key: checker.check() for key, checker in self._checkers.items()}

        # Transform results to match legacy API structure expected by UI
        return {
            "root_presence": {
                "found": results["root_presence"]["found"],
                "message": results["root_presence"]["message"],
            },
            "selinux": results["selinux"]["status"],
            "ld_preload": {
                "active": results["ld_preload"]["active"],
                "message": results["ld_preload"]["message"],
            },
            "termux_suid": results["termux_suid"]["message"],
        }
