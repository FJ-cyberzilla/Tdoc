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

    assert "activity" in results
    assert results["activity"]["status"] == "STATIONARY"
    assert "environment" in results
    assert results["environment"]["Magnetometer"]["values"] == [1, 2, 3]
    assert results["environment"]["Hall IC"]["values"] == [0]
    assert "orientation" in results  # Ensure new analyzer is integrated
    assert "raw" in results


def test_security_status():
    """Test security status check."""
    mock_fetcher = MagicMock(spec=TermuxSensorFetcher)
    service = SensorHubService(fetcher=mock_fetcher)
    # Depending on the test environment, this might be SECURE or VULNERABLE
    # We just want to ensure it doesn't crash
    status = service.get_security_status()
    assert "biometric_available" in status
    assert "lock_state" in status
