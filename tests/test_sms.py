from unittest.mock import MagicMock, patch

import pytest

from src.services.network.sms import SMSChecker


@pytest.fixture
def checker():
    return SMSChecker()

def test_analyze_empty_messages(checker):
    result = checker.analyze_messages([])
    assert result["total_messages"] == 0
    assert result["sent_recv_ratio"] == "0/0"

def test_analyze_complex_messages(checker):
    mock_messages = [
        {"address": "123", "body": "Hello", "type": 1, "date": 1700000000000},
        {"address": "456", "body": "URL http://malicious.com", "type": 1, "date": 1700000000000},
        {"address": "456", "body": "URL http://malicious.com", "type": 1, "date": 1700000000000},
        {"address": "456", "body": "URL http://malicious.com", "type": 1, "date": 1700000000000},
        {"address": "789", "body": "Sent msg", "type": 2, "date": 1700000000000},
    ]
    result = checker.analyze_messages(mock_messages)
    assert result["total_messages"] == 5
    assert len(result["risky_domains"]) > 0
    assert result["sent_recv_ratio"] == "1/4"

def test_sms_checker_failure_handling():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        checker = SMSChecker()
        result = checker.check()
        assert result["error"] == "Failed to access SMS"

