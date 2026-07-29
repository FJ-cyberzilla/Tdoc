import subprocess
from unittest.mock import MagicMock, patch

from src.services.network.hotspot import HotspotChecker


def test_hotspot_checker_wifi_active():
    checker = HotspotChecker()
    mock_res = MagicMock(returncode=0, stdout="1: lo: <...> \n 2: ap0: <UP,BROADCAST> \n")
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["active"] is True
        assert "Wi-Fi Hotspot" in data["type"]

def test_hotspot_checker_usb_active():
    checker = HotspotChecker()
    mock_res = MagicMock(returncode=0, stdout="1: lo: <...> \n 3: rndis0: <UP> \n")
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["active"] is True
        assert "USB Tethering" in data["type"]

def test_hotspot_checker_disabled():
    checker = HotspotChecker()
    mock_res = MagicMock(returncode=0, stdout="1: lo: <...> \n 2: wlan0: <UP> \n")
    
    with patch("subprocess.run", return_value=mock_res):
        data = checker.check()
        assert data["active"] is False

def test_hotspot_checker_error():
    checker = HotspotChecker()
    # HotspotChecker catches SubprocessError and OSError, not generic Exception
    with patch("subprocess.run", side_effect=subprocess.SubprocessError):
        data = checker.check()
        assert data["active"] is False
        assert data["type"] == "Error"
