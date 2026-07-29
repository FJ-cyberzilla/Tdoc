"""
Tests for TermuxApiService.
"""

import unittest
from unittest.mock import patch

from src.services.android.termux_api_service import TermuxApiService


class TestTermuxApiService(unittest.TestCase):
    """Unit tests for TermuxApiService."""

    @patch("src.core.command_runner.CommandRunner.run_command")
    def test_run(self, mock_run):
        """Test comprehensive Termux API data collection."""
        mock_run.side_effect = ["Battery", "WiFi", "Telephony", "Location"]
        service = TermuxApiService()
        result = service.run()

        self.assertEqual(result["battery"], "Battery")
        self.assertEqual(result["wifi"], "WiFi")
        self.assertEqual(result["telephony"], "Telephony")
        self.assertEqual(result["location"], "Location")
        self.assertEqual(mock_run.call_count, 4)
