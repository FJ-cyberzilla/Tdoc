from unittest.mock import MagicMock, patch

from src.services.network.wifi import WifiChecker


def test_wifi_checker_connected():
    mock_data = {"supplicant_state": "COMPLETED", "ip": "192.168.1.5", "ssid": "TestWiFi"}
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=str(mock_data).replace("'", '"'))
        checker = WifiChecker()
        result = checker.check()
        assert result["status"] == "CONNECTED"
        assert result["ssid"] == "TestWiFi"


def test_wifi_checker_off():
    mock_data = {"supplicant_state": "UNINITIALIZED"}
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=str(mock_data).replace("'", '"'))
        checker = WifiChecker()
        result = checker.check()
        assert result["status"] == "OFF"
