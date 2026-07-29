import json
from unittest.mock import MagicMock, patch

from src.services.network.wifi import WifiChecker


def test_wifi_checker_connected():
    checker = WifiChecker()
    mock_data = {"supplicant_state": "COMPLETED", "ip": "192.168.1.5", "ssid": "MyWiFi"}
    mock_res = MagicMock(returncode=0, stdout=json.dumps(mock_data))
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["status"] == "CONNECTED"
        assert data["ssid"] == "MyWiFi"

def test_wifi_checker_disconnected():
    checker = WifiChecker()
    mock_data = {"supplicant_state": "DISCONNECTED", "ip": "0.0.0.0"}
    mock_res = MagicMock(returncode=0, stdout=json.dumps(mock_data))
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["status"] == "DISCONNECTED"

def test_wifi_checker_off():
    checker = WifiChecker()
    mock_data = {"supplicant_state": "UNINITIALIZED"}
    mock_res = MagicMock(returncode=0, stdout=json.dumps(mock_data))
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["status"] == "OFF"

def test_wifi_checker_error():
    checker = WifiChecker()
    mock_res = MagicMock(returncode=1, stdout="")
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["status"] == "ERROR"
