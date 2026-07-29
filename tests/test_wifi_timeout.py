import subprocess
from unittest.mock import patch

from src.services.network.wifi import WifiChecker


def test_wifi_checker_timeout():
    checker = WifiChecker()
    # Mock subprocess.run to raise a TimeoutExpired error
    cmd = ["termux-wifi-connectioninfo"]
    side_effect = subprocess.TimeoutExpired(cmd=cmd, timeout=2)
    with patch("subprocess.run", side_effect=side_effect):
        data = checker.check()
        assert data["status"] == "ERROR"
