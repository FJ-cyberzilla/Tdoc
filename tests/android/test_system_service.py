"""
Tests for SystemService.
"""

import unittest
from unittest.mock import patch

from src.services.android.system_service import SystemService


class TestSystemService(unittest.TestCase):
    """Unit tests for SystemService."""

    @patch("src.core.command_runner.CommandRunner.run_command")
    def test_run(self, mock_run):
        """Test comprehensive system data collection."""
        mock_run.side_effect = ["Uptime", "PS", "Disk", "Battery"]
        service = SystemService()
        result = service.run()

        self.assertEqual(result["uptime"], "Uptime")
        self.assertEqual(result["ps"], "PS")
        self.assertEqual(result["disk"], "Disk")
        self.assertEqual(result["dumpsys_battery"], "Battery")
        self.assertEqual(mock_run.call_count, 4)
