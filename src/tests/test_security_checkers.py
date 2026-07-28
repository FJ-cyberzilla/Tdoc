from unittest.mock import patch

from src.services.security_checkers import (
    LDPreloadChecker,
    RootPresenceChecker,
    SELinuxStatusChecker,
    SUIDBinaryChecker,
)


def test_root_presence_checker_no_su():
    with patch("os.stat", side_effect=FileNotFoundError):
        checker = RootPresenceChecker()
        result = checker.check()
        assert result["found"] is False
        assert "PRISTINE" in result["message"]


def test_selinux_checker_enforcing():
    with patch("subprocess.check_output", return_value=b"Enforcing"):
        checker = SELinuxStatusChecker()
        result = checker.check()
        assert "Enforcing" in result["status"]


def test_ld_preload_checker_inactive():
    with patch.dict("os.environ", {"LD_PRELOAD": ""}):
        checker = LDPreloadChecker()
        result = checker.check()
        assert result["active"] is False
        assert "INACTIVE" in result["message"]


def test_suid_checker_pristine():
    with patch("os.path.isdir", return_value=True), patch("os.scandir", return_value=[]):
        checker = SUIDBinaryChecker()
        result = checker.check()
        assert "Pristine" in result["message"]
