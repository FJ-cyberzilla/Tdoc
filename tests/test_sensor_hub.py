"""
Tests for Sensor Hub Service.
"""

from unittest.mock import MagicMock

from src.services.fetcher import TermuxSensorFetcher
from src.services.sensor_hub import SensorHubService


def test_sensor_hub_integration():
    """Verify that SensorHubService integrates fetcher and analyzers."""
    mock_fetcher = MagicMock(spec=TermuxSensorFetcher)
    mock_fetcher.get_data.return_value = {
        "Accelerometer": {"values": [0, 0, 9.8]},
        "Magnetometer": {"values": [1, 2, 3]},
        "Hall IC": {"values": [0]},
        "Light": {"values": [50.0]},
    }

    # Use real analyzers for integration
    service = SensorHubService(fetcher=mock_fetcher)

    results = service.run()

    assert results.activity.status == "STATIONARY"
    assert results.environment.magnetometer.values == [1, 2, 3]
    assert results.environment.hall_ic.values == [0]
    assert results.orientation is not None
    assert results.raw is not None


def test_security_status():
    """Test security status check."""
    mock_fetcher = MagicMock(spec=TermuxSensorFetcher)
    service = SensorHubService(fetcher=mock_fetcher)
    # Depending on the test environment, this might be SECURE or VULNERABLE
    # We just want to ensure it doesn't crash
    status = service.get_security_status()
    assert isinstance(status.biometric_available, bool)
    assert isinstance(status.lock_state, str)
