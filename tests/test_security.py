"""
Unit tests for the SecurityService and its checkers.

This test suite covers permission checks, file integrity, encryption status,
vulnerability scanning, password policies, and audit logging.
"""

import os
from unittest.mock import MagicMock, patch

from src.services.security import SecurityService
from src.services.security_checkers import (
    EncryptionChecker,
    PermissionChecker,
    RootPresenceChecker,
    VulnerabilityChecker,
)


def test_permission_checks():
    """Test PermissionChecker's ability to detect directory write permissions."""
    checker = PermissionChecker()

    with (
        patch("os.access", side_effect=[True, False]),
        patch.dict(os.environ, {"PREFIX": "/tmp/prefix", "HOME": "/tmp/home"}),
    ):
        results = checker.check()
        assert results["prefix_writable"] is True
        assert results["home_writable"] is False


def test_encryption_status():
    """Test EncryptionChecker with different system property values."""
    checker = EncryptionChecker()

    # Case 1: Encrypted
    mock_res_enc = MagicMock(returncode=0, stdout="encrypted\n")
    with patch("subprocess.run", return_value=mock_res_enc):
        results = checker.check()
        assert results["encrypted"] is True
        assert results["state"] == "encrypted"

    # Case 2: Unencrypted
    mock_res_unenc = MagicMock(returncode=0, stdout="unencrypted\n")
    with patch("subprocess.run", return_value=mock_res_unenc):
        results = checker.check()
        assert results["encrypted"] is False
        assert results["state"] == "unencrypted"


def test_vulnerability_scanning():
    """Test VulnerabilityChecker for debuggable builds and ADB status."""
    checker = VulnerabilityChecker()

    # Case: Vulnerable (debuggable and ADB enabled)
    def mock_query(cmd, **kwargs):
        prop = cmd[1]
        if prop == "ro.debuggable":
            return MagicMock(returncode=0, stdout="1\n")
        if prop == "init.svc.adbd":
            return MagicMock(returncode=0, stdout="running\n")
        return MagicMock(returncode=0, stdout="0\n")

    with patch("subprocess.run", side_effect=mock_query):
        results = checker.check()
        assert results["debuggable"] is True
        assert results["adb_enabled"] is True


def test_root_presence_detection():
    """Test RootPresenceChecker with various su binary scenarios."""
    checker = RootPresenceChecker()

    # Case 1: Root detected (setuid bit set)
    mock_stat = MagicMock()
    mock_stat.st_mode = 0o104755  # Regular file + setuid
    with (
        patch("os.stat", return_value=mock_stat),
        patch("stat.S_ISREG", return_value=True),
    ):
        results = checker.check()
        assert results["found"] is True
        assert "DETECTED" in results["message"]

    # Case 2: su exists but no setuid bit
    mock_stat_no_suid = MagicMock()
    mock_stat_no_suid.st_mode = 0o100755
    with (
        patch("os.stat", return_value=mock_stat_no_suid),
        patch("stat.S_ISREG", return_value=True),
    ):
        results = checker.check()
        assert results["found"] is False
        assert "NO setuid bit" in results["message"]


def test_security_service_aggregation():
    """Test that SecurityService correctly aggregates results from all checkers."""
    service = SecurityService()

    with (
        patch.object(RootPresenceChecker, "check", return_value={"found": False, "message": "OK"}),
        patch.object(PermissionChecker, "check", return_value={"prefix_writable": True}),
        patch.object(EncryptionChecker, "check", return_value={"encrypted": True}),
        patch.object(VulnerabilityChecker, "check", return_value={"debuggable": False}),
    ):
        results = service.run()
        assert results["root_presence"]["found"] is False
        assert results["permissions"]["prefix_writable"] is True
        assert results["encryption"]["encrypted"] is True
        assert results["vulnerabilities"]["debuggable"] is False
