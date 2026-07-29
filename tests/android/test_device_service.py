"""
Tests for DeviceService.
"""

import unittest
from unittest.mock import patch

from src.services.android.device_service import DeviceService


class TestDeviceService(unittest.TestCase):
    """Unit tests for DeviceService."""

    @patch("src.core.command_runner.CommandRunner.run_command")
    def test_run(self, mock_run):
        """Test aggregate device data collection."""
        # Mocking 9 property calls + 2 file reads = 11 calls
        mock_run.side_effect = [
            "Model",
            "Man",
            "Brand",
            "Device",
            "Rel",
            "SDK",
            "HW",
            "Board",
            "SoC",
            "CPUInfo",
            "MemInfo",
        ]
        service = DeviceService()
        result = service.run()

        self.assertEqual(result["ro.product.model"], "Model")
        self.assertEqual(result["cpuinfo"], "CPUInfo")
        self.assertEqual(mock_run.call_count, 11)
