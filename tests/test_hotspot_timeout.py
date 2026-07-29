import subprocess
from unittest.mock import patch

from src.services.network.hotspot import HotspotChecker


def test_hotspot_checker_timeout():
    checker = HotspotChecker()
    patch_path = "subprocess.run"
    side_effect = subprocess.TimeoutExpired(cmd=["ip", "link"], timeout=2)
    with patch(patch_path, side_effect=side_effect):
        data = checker.check()
        assert data["active"] is False
        assert data["type"] == "Error"
