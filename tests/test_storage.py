"""
Unit tests for the StorageMonitor.

This test suite covers free storage estimation and write speed measurement.
"""

from unittest.mock import MagicMock, patch

from src.services.storage import StorageMonitor


def test_storage_monitor_run():
    """Test StorageMonitor correctly measures free space and write speed."""
    monitor = StorageMonitor()

    # Mock shutil.disk_usage and time.time
    with (
        patch("shutil.disk_usage", return_value=(0, 0, 1024**3 * 50)),
        patch("os.urandom", return_value=b"0" * (1024 * 1024 * 25)),
        patch("time.time", side_effect=[0, 0.5]),
        patch("builtins.open", MagicMock()),
        patch("os.fsync", MagicMock()),
        patch("os.remove", MagicMock()),
    ):
        results = monitor.run()
        assert results["free_storage_gb"] == 50.0
        assert results["write_speed_mb_s"] == 50.0  # 25MB / 0.5s = 50MB/s


def test_storage_monitor_errors():
    """Test StorageMonitor handles OS errors gracefully."""
    monitor = StorageMonitor()

    # Mock OSError for both operations
    with (
        patch("shutil.disk_usage", side_effect=OSError),
        patch("builtins.open", side_effect=OSError),
    ):
        results = monitor.run()
        assert results["free_storage_gb"] is None
        assert results["write_speed_mb_s"] is None
