import subprocess
from unittest.mock import patch

from src.services.environment.sensors import SensorCollector


def test_sensor_collector_timeout():
    collector = SensorCollector()
    # The first call is "termux-sensor -l"
    cmd = ["termux-sensor", "-l"]
    side_effect = subprocess.TimeoutExpired(cmd=cmd, timeout=2)
    with patch("subprocess.run", side_effect=side_effect):
        data = collector.get_sensor_data()
        assert "error" in data
        assert data["error"] == "Failed to list sensors"
