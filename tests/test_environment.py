"""
Test suite for the EnvironmentService.

This module verifies that the application correctly detects and reports
details about the operating environment, distinguishing between Android/Termux
and other platforms.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.services.environment import EnvironmentService


@pytest.fixture
def environment_service():
    """Provides a fresh instance of EnvironmentService for each test."""
    return EnvironmentService()


def test_run_android(environment_service):
    """
    Verifies environment detection when running on an Android/Termux system.

    Mocks:
        - shutil.which: Simulates presence of Android/Termux tools (getprop, termux-battery-status).
        - platform.system: Returns 'Linux'.
        - platform.machine: Returns 'aarch64'.
        - os.environ.get: Returns a standard locale.
        - os.path.exists: Simulates that the Termux PREFIX exists.
        - subprocess.run: Simulates 'getprop' returning device info.

    Expects:
        - is_android: True
        - manufacturer: 'TEST_VALUE' (from getprop mock)
        - api_connected: True
    """
    # Mock dependencies
    with (
        patch(
            "shutil.which",
            side_effect=lambda x: {
                "getprop": "/system/bin/getprop",
                "termux-battery-status": "/usr/bin/termux-battery-status",
            }.get(x),
        ),
        patch("platform.system", return_value="Linux"),
        patch("platform.machine", return_value="aarch64"),
        patch("os.environ.get", return_value="en_US.UTF-8"),
        patch("os.path.exists", return_value=True),
        patch("subprocess.run") as mock_subprocess,
    ):
        mock_subprocess.return_value = MagicMock(stdout="TEST_VALUE", returncode=0)

        # Execute
        results = environment_service.run()

        # Assert
        assert results["is_android"] is True
        assert results["manufacturer"] == "TEST_VALUE"
        assert results["api_connected"] is True
        assert results["boot_status"] is True


def test_run_non_android(environment_service):
    """
    Verifies environment detection when running on a non-Android system (e.g., macOS).

    Mocks:
        - shutil.which: Returns None (no Android tools).
        - platform.system: Returns 'Darwin'.
        - platform.release: Returns '22.0.0'.
        - os.path.exists: Returns False for Termux-specific paths.

    Expects:
        - is_android: False
        - manufacturer: 'Generic'
    """
    # Mock setup
    with (
        patch("shutil.which", return_value=None),
        patch("platform.system", return_value="Darwin"),
        patch("platform.machine", return_value="x86_64"),
        patch("platform.release", return_value="22.0.0"),
        patch("os.path.exists", return_value=False),
    ):
        # Execute
        results = environment_service.run()

        # Assert
        _assert_non_android(results)


def _assert_non_android(results):
    """Helper to validate results for a generic non-Android environment."""
    assert results["is_android"] is False
    assert results["manufacturer"] == "Generic"
    assert results["api_connected"] is False
    assert results["boot_status"] is False
    assert results["version"] == "22.0.0"
