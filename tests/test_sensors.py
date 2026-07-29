from unittest.mock import MagicMock, patch

from src.services.environment.sensors import SensorCollector


def test_sensor_collector_success():
    mock_list = {"sensors": ["Accelerometer", "Light"]}
    mock_data = {"Accelerometer": {"x": 0.1}, "Light": {"lux": 100}}

    with patch("subprocess.run") as mock_run:
        # Mock first call (list), second call (data)
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=str(mock_list).replace("'", '"')),
            MagicMock(returncode=0, stdout=str(mock_data).replace("'", '"')),
        ]

        collector = SensorCollector()
        result = collector.get_sensor_data()
        assert "Accelerometer" in result
        assert result["Light"]["lux"] == 100
