from unittest.mock import MagicMock, patch

import pytest

from src.services.environment import EnvironmentService


@pytest.fixture
def environment_service():
    return EnvironmentService()


def test_run_android(environment_service):
    # Mock dependencies
    with (
        patch(
            "shutil.which",
            side_effect=lambda x: {
                "getprop": "/system/bin/getprop",
                "termux-battery-status": "/usr/bin/termux-battery-status",
            }.get(x, None),
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
    assert results["is_android"] is False
    assert results["manufacturer"] == "Generic"
    assert results["api_connected"] is False
    assert results["boot_status"] is False
    assert results["version"] == "22.0.0"
