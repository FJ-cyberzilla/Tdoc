import json
from unittest.mock import MagicMock, patch

from src.services.environment.sensors import SensorCollector


def test_sensor_collector_success():
    collector = SensorCollector()

    # Mock list and data calls
    sensors = ["Accelerometer", "Light"]
    mock_list_res = MagicMock(returncode=0, stdout=json.dumps({"sensors": sensors}))
    data_mock = {"Accelerometer": {"values": [1, 2, 3]}}
    mock_data_res = MagicMock(returncode=0, stdout=json.dumps(data_mock))

    with patch("subprocess.run", side_effect=[mock_list_res, mock_data_res]):
        data = collector.get_sensor_data()
        assert "Accelerometer" in data
        assert data["Accelerometer"]["values"] == [1, 2, 3]


def test_sensor_collector_list_failure():
    collector = SensorCollector()

    # Mock list failure
    mock_list_res = MagicMock(returncode=1, stdout="")

    with patch("subprocess.run", return_value=mock_list_res):
        data = collector.get_sensor_data()
        assert "error" in data
        assert data["error"] == "Failed to list sensors"


def test_sensor_collector_data_failure():
    collector = SensorCollector()

    # Mock list success, data failure
    mock_list_res = MagicMock(returncode=0, stdout=json.dumps({"sensors": ["Accelerometer"]}))
    mock_data_res = MagicMock(returncode=1, stdout="")

    with patch("subprocess.run", side_effect=[mock_list_res, mock_data_res]):
        data = collector.get_sensor_data()
        assert "error" in data
        assert data["error"] == "Failed to fetch sensor data"
