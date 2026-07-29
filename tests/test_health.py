"""
Test suite for the HealthService and its monitors (Storage and Battery).

This module contains unit tests that verify the correct operation of system health
monitoring, using mocks to simulate hardware status and OS responses.
"""

from unittest.mock import MagicMock, patch

from src.services.battery import BatteryMonitor
from src.services.health import HealthService
from src.services.storage import StorageMonitor


def test_storage_monitor():
    """
    Tests the StorageMonitor's ability to calculate free space and write speed.

    Mocks:
        - shutil.disk_usage: Simulates disk space stats.
        - os.urandom: Simulates writing a test file for speed measurement.
        - time.time: Simulates duration of the write operation.
        - builtins.open, os.fsync, os.remove: Prevents actual file I/O.
    """
    monitor = StorageMonitor()
    with (
        patch("shutil.disk_usage", return_value=(100, 40, 60)),
        patch("os.urandom", return_value=b"0" * 25 * 1024 * 1024),
        patch("time.time", side_effect=[0, 1]),
        patch("builtins.open", MagicMock()),
        patch("os.fsync", MagicMock()),
        patch("os.remove", MagicMock()),
    ):
        results = monitor.run()
        # Note: The calculation in the source uses 1024**3 for GB conversion
        assert results["free_storage_gb"] == 60 / (1024**3)
        assert results["write_speed_mb_s"] == 25.0


def test_battery_monitor_termux_api():
    """
    Tests the BatteryMonitor's parsing of termux-battery-status output.

    Mocks:
        - shutil.which: Simulates presence of the termux-battery-status tool.
        - subprocess.run: Simulates the JSON output of the tool.
    """
    monitor = BatteryMonitor()
    mock_res = MagicMock(
        returncode=0, stdout='{"percentage": 85, "status": "discharging", "temperature": 35.5}'
    )

    with (
        patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
        patch("subprocess.run", return_value=mock_res),
    ):
        results = monitor.run()
        assert results["capacity"] == "85%"
        assert results["status"] == "DISCHARGING"
        assert results["temp"] == "35.5°C"


def test_health_service_orchestration():
    """
    Tests that HealthService correctly aggregates data from multiple monitors.

    Mocks:
        - StorageMonitor.run: Returns static storage data.
        - BatteryMonitor.run: Returns static battery data.
    """
    service = HealthService()
    with (
        patch.object(
            StorageMonitor, "run", return_value={"free_storage_gb": 10.0, "write_speed_mb_s": 5.0}
        ),
        patch.object(
            BatteryMonitor,
            "run",
            return_value={"capacity": "90%", "temp": "30°C", "status": "CHARGING"},
        ),
    ):
        results = service.run()
        assert results["free_storage_gb"] == 10.0
        assert results["write_speed_mb_s"] == 5.0
        assert results["battery"]["capacity"] == "90%"
