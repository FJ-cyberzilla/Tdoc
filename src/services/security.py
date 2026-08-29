"""
TDoc Security Subsystem – Hardened Privilege Audit
"""

from src.interfaces import DiagnosticService
from src.services.security_checkers import (
    EncryptionChecker,
    LDPreloadChecker,
    PermissionChecker,
    RootPresenceChecker,
    SELinuxStatusChecker,
    SUIDBinaryChecker,
    VulnerabilityChecker,
)
from src.services.security_models import SecurityTelemetry


class SecurityService(DiagnosticService):
    """Service to evaluate system security and privilege status."""

    def __init__(self) -> None:
        self._root_checker = RootPresenceChecker()
        self._selinux_checker = SELinuxStatusChecker()
        self._ld_preload_checker = LDPreloadChecker()
        self._suid_checker = SUIDBinaryChecker()
        self._permissions_checker = PermissionChecker()
        self._encryption_checker = EncryptionChecker()
        self._vulnerabilities_checker = VulnerabilityChecker()

    def run(self) -> SecurityTelemetry:
        """Executes host privilege security audit with real system inspection."""
        return SecurityTelemetry(
            root_presence=self._root_checker.check(),
            selinux=self._selinux_checker.check(),
            ld_preload=self._ld_preload_checker.check(),
            suid=self._suid_checker.check(),
            permissions=self._permissions_checker.check(),
            encryption=self._encryption_checker.check(),
            vulnerabilities=self._vulnerabilities_checker.check(),
        )
