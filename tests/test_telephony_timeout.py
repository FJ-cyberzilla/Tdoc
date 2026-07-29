import subprocess
from unittest.mock import patch

from src.services.network.telephony import TelephonyChecker


def test_telephony_checker_timeout():
    checker = TelephonyChecker()
    # Mock subprocess.run to raise TimeoutExpired for one of the commands
    cmd = ["termux-telephony-deviceinfo"]
    side_effect = subprocess.TimeoutExpired(cmd=cmd, timeout=2)
    with patch("subprocess.run", side_effect=side_effect):
        data = checker.check()
        # TelephonyChecker catches all Exceptions and sets the command result to an error dict
        assert "error" in data["deviceinfo"]
        assert data["deviceinfo"]["error"] == "Tool not found or execution failed"
