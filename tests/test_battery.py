"""
Unit tests for the BatteryMonitor service.

This test suite covers battery status checking, charge level monitoring,
battery health validation, threshold alerts, and error scenarios.
"""

import json
from unittest.mock import MagicMock, patch

from src.services.battery import BatteryMonitor


def test_battery_status_checking():
    """Test battery status checking with different statuses (CHARGING, DISCHARGING, FULL, etc.)."""
    monitor = BatteryMonitor()
    statuses = ["CHARGING", "discharging", "full", "not charging"]

    for status in statuses:
        mock_stdout = json.dumps(
            {
                "percentage": 80,
                "status": status,
                "temperature": 25.5,
                "voltage": 4000000,
                "current_now": 500000,
            }
        )
        mock_res = MagicMock(returncode=0, stdout=mock_stdout)

        with (
            patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
            patch("subprocess.run", return_value=mock_res),
        ):
            results = monitor.run()
            assert results["status"] == status.upper()


def test_charge_level_monitoring():
    """Test charge level monitoring across various levels (0%, 5%, 50%, 100%)."""
    monitor = BatteryMonitor()
    percentages = [0, 5, 50, 100]

    for pct in percentages:
        mock_stdout = json.dumps(
            {
                "percentage": pct,
                "status": "DISCHARGING",
                "temperature": 25.5,
                "voltage": 3800000,
                "current_now": -200000,
            }
        )
        mock_res = MagicMock(returncode=0, stdout=mock_stdout)

        with (
            patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
            patch("subprocess.run", return_value=mock_res),
        ):
            results = monitor.run()
            assert results["capacity"] == f"{pct}%"
            assert results["cap_num"] == pct


def test_battery_health_validation():
    """Test battery health validation, including temperature scale conversion (tenths of C)."""
    monitor = BatteryMonitor()

    # Case 1: Standard temperature (already in degrees Celsius, e.g., 35.5)
    mock_res_std = MagicMock(
        returncode=0,
        stdout=json.dumps(
            {
                "percentage": 85,
                "status": "DISCHARGING",
                "temperature": 35.5,
                "voltage": 4100000,
                "current_now": -150000,
            }
        ),
    )

    # Case 2: Temperature in tenths of Celsius (e.g., 355 -> should be divided by 10)
    mock_res_tenths = MagicMock(
        returncode=0,
        stdout=json.dumps(
            {
                "percentage": 85,
                "status": "DISCHARGING",
                "temperature": 355,
                "voltage": 4100000,
                "current_now": -150000,
            }
        ),
    )

    with patch("shutil.which", return_value="/usr/bin/termux-battery-status"):
        with patch("subprocess.run", return_value=mock_res_std):
            results = monitor.run()
            assert results["temp_num"] == 35.5
            assert results["temp"] == "35.5°C"

        with patch("subprocess.run", return_value=mock_res_tenths):
            results = monitor.run()
            assert results["temp_num"] == 35.5
            assert results["temp"] == "35.5°C"


def test_threshold_alerts():
    """Test battery health and threshold alerts logic.

    Checks:
        - High temperature threshold (> 45°C)
        - Low battery threshold (< 15%)
    """
    # High Temperature Case
    monitor = BatteryMonitor()
    mock_high_temp = MagicMock(
        returncode=0,
        stdout=json.dumps(
            {
                "percentage": 80,
                "status": "CHARGING",
                "temperature": 48.5,
                "voltage": 4300000,
                "current_now": 1200000,
            }
        ),
    )
    with (
        patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
        patch("subprocess.run", return_value=mock_high_temp),
    ):
        results = monitor.run()
        # Evaluate warning conditions
        is_temp_warning = results["temp_num"] > 45.0
        assert is_temp_warning is True

    # Low Battery Case
    mock_low_bat = MagicMock(
        returncode=0,
        stdout=json.dumps(
            {
                "percentage": 10,
                "status": "DISCHARGING",
                "temperature": 28.0,
                "voltage": 3500000,
                "current_now": -300000,
            }
        ),
    )
    with (
        patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
        patch("subprocess.run", return_value=mock_low_bat),
    ):
        results = monitor.run()
        is_low_battery_warning = results["cap_num"] < 15.0
        assert is_low_battery_warning is True


def test_error_scenarios():
    """
    Test battery error scenarios including subprocess failure, JSON decode error,
    and missing binary.
    """
    monitor = BatteryMonitor()

    # Case 1: missing termux-battery-status (falls back to disconnected status)
    with patch("shutil.which", return_value=None):
        results = monitor.run()
        assert results["status"] == "DISCONNECTED"
        assert results["capacity"] == "0%"

    # Case 2: subprocess fails (returns non-zero)
    mock_fail = MagicMock(returncode=1, stdout="")
    with (
        patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
        patch("subprocess.run", return_value=mock_fail),
    ):
        results = monitor.run()
        assert results["status"] == "DISCONNECTED"

    # Case 3: JSON decode error
    mock_invalid_json = MagicMock(returncode=0, stdout="{invalid_json}")
    with (
        patch("shutil.which", return_value="/usr/bin/termux-battery-status"),
        patch("subprocess.run", return_value=mock_invalid_json),
    ):
        results = monitor.run()
        assert results["status"] == "DISCONNECTED"
