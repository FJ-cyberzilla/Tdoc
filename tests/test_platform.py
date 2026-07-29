"""
Unit tests for the PlatformService.

This test suite covers the aggregation of environment and health services.
"""

from unittest.mock import patch

from src.services.platform import PlatformService


def test_platform_service_run():
    """Test that PlatformService aggregates data correctly."""
    with (
        patch("src.services.platform.EnvironmentService") as MockEnv,
        patch("src.services.platform.HealthService") as MockHealth,
    ):
        mock_env_instance = MockEnv.return_value
        mock_env_instance.run.return_value = {"os": "android"}

        mock_health_instance = MockHealth.return_value
        mock_health_instance.run.return_value = {"battery": "OK"}

        service = PlatformService()
        results = service.run()

        assert results["environment"] == {"os": "android"}
        assert results["health"] == {"battery": "OK"}
        mock_env_instance.run.assert_called_once()
        mock_health_instance.run.assert_called_once()
