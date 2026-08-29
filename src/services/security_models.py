"""
Typed data models for security telemetry.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RootPresenceResult:
    found: bool
    message: str


@dataclass(frozen=True)
class SELinuxResult:
    status: str


@dataclass(frozen=True)
class LDPreloadResult:
    active: bool
    message: str


@dataclass(frozen=True)
class SUIDBinaryResult:
    message: str


@dataclass(frozen=True)
class PermissionResult:
    prefix_writable: bool
    home_writable: bool
    prefix: str


@dataclass(frozen=True)
class EncryptionResult:
    encrypted: bool
    state: str
    type: str


@dataclass(frozen=True)
class VulnerabilityResult:
    debuggable: bool
    secure: bool
    adb_enabled: bool


@dataclass(frozen=True)
class SecurityTelemetry:
    root_presence: RootPresenceResult
    selinux: SELinuxResult
    ld_preload: LDPreloadResult
    suid: SUIDBinaryResult
    permissions: PermissionResult
    encryption: EncryptionResult
    vulnerabilities: VulnerabilityResult
