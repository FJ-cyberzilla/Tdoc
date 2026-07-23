from unittest.mock import MagicMock, patch
from src.services.health import HealthService
from src.services.storage import StorageMonitor
from src.services.battery import BatteryMonitor


def test_storage_monitor():
    monitor = StorageMonitor()
    with patch("shutil.disk_usage", return_value=(100, 40, 60)), patch(
        "os.urandom", return_value=b"0" * 25 * 1024 * 1024
    ), patch("time.time", side_effect=[0, 1]), patch("builtins.open", MagicMock()), patch(
        "os.fsync", MagicMock()
    ), patch("os.remove", MagicMock()):
        results = monitor.run()
        assert results["free_storage_gb"] == 60 / (1024**3)
        assert results["write_speed_mb_s"] == 25.0


def test_battery_monitor_termux_api():
    monitor = BatteryMonitor()
    mock_res = MagicMock(
        returncode=0, stdout='{"percentage": 85, "status": "discharging", "temperature": 35.5}'
    )

    with patch("shutil.which", return_value="/usr/bin/termux-battery-status"), patch(
        "subprocess.run", return_value=mock_res
    ):
        results = monitor.run()
        assert results["capacity"] == "85%"
        assert results["status"] == "DISCHARGING"
        assert results["temp"] == "35.5°C"


def test_health_service_orchestration():
    service = HealthService()
    with patch.object(
        StorageMonitor, "run", return_value={"free_storage_gb": 10.0, "write_speed_mb_s": 5.0}
    ), patch.object(
        BatteryMonitor,
        "run",
        return_value={"capacity": "90%", "temp": "30°C", "status": "CHARGING"},
    ):
        results = service.run()
        assert results["free_storage_gb"] == 10.0
        assert results["write_speed_mb_s"] == 5.0
        assert results["battery"]["capacity"] == "90%"
