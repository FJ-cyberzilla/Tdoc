"""
Test suite for the security checker services.

Verifies that root presence, SELinux status, LD_PRELOAD, and SUID binary checks
behave correctly under various simulated system states.
"""

from unittest.mock import patch

from src.services.security_checkers import (
    LDPreloadChecker,
    RootPresenceChecker,
    SELinuxStatusChecker,
    SUIDBinaryChecker,
)


def test_root_presence_checker_no_su():
    """
    Tests RootPresenceChecker when no 'su' binary is found on the system.

    Mocks:
        - os.stat: Raises FileNotFoundError for all paths to simulate absence.
    """
    with patch("os.stat", side_effect=FileNotFoundError):
        checker = RootPresenceChecker()
        result = checker.check()
        assert result["found"] is False
        assert "PRISTINE" in result["message"]


def test_selinux_checker_enforcing():
    """
    Tests SELinuxStatusChecker when SELinux is in 'Enforcing' mode.

    Mocks:
        - subprocess.check_output: Simulates 'getenforce' returning 'Enforcing'.
    """
    with patch("subprocess.check_output", return_value=b"Enforcing"):
        checker = SELinuxStatusChecker()
        result = checker.check()
        assert "Enforcing" in result["status"]


def test_ld_preload_checker_inactive():
    """
    Tests LDPreloadChecker when the LD_PRELOAD environment variable is empty.

    Mocks:
        - os.environ: Patched to ensure LD_PRELOAD is an empty string.
    """
    with patch.dict("os.environ", {"LD_PRELOAD": ""}):
        checker = LDPreloadChecker()
        result = checker.check()
        assert result["active"] is False
        assert "INACTIVE" in result["message"]


def test_suid_checker_pristine():
    """
    Tests SUIDBinaryChecker when the bin directory contains no SUID/SGID files.

    Mocks:
        - os.path.isdir: Simulates that the bin directory exists.
        - os.scandir: Simulates an empty directory.
    """
    with patch("os.path.isdir", return_value=True), patch("os.scandir", return_value=[]):
        checker = SUIDBinaryChecker()
        result = checker.check()
        assert "Pristine" in result["message"]
