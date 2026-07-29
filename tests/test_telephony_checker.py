import json
from unittest.mock import MagicMock, patch

from src.services.network.telephony import TelephonyChecker


def test_telephony_checker_success():
    checker = TelephonyChecker()

    # Mock successful calls
    mock_responses = [
        MagicMock(returncode=0, stdout=json.dumps({"network_operator_name": "Carrier"})),
        MagicMock(returncode=0, stdout=json.dumps({"dbm": -80})),
        MagicMock(returncode=0, stdout=json.dumps([{"type": "LTE"}])),
    ]

    with patch("subprocess.run", side_effect=mock_responses):
        data = checker.check()
        assert "deviceinfo" in data
        assert "signalstrength" in data
        assert "cellinfo" in data
        assert data["signalstrength"]["dbm"] == -80


def test_telephony_checker_partial_failure():
    checker = TelephonyChecker()

    # Mock one failure
    mock_responses = [
        MagicMock(returncode=0, stdout=json.dumps({"network_operator_name": "Carrier"})),
        MagicMock(returncode=1, stdout=""),  # signalstrength fails
        MagicMock(returncode=0, stdout=json.dumps([{"type": "LTE"}])),
    ]

    with patch("subprocess.run", side_effect=mock_responses):
        data = checker.check()
        assert "error" in data["signalstrength"]
        assert data["deviceinfo"]["network_operator_name"] == "Carrier"
