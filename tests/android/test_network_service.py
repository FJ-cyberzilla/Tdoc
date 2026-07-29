"""
Tests for NetworkService.
"""

import unittest
from unittest.mock import patch

from src.services.android.network_service import NetworkService


class TestNetworkService(unittest.TestCase):
    """Unit tests for NetworkService."""

    @patch("src.core.command_runner.CommandRunner.run_command")
    def test_run(self, mock_run):
        """Test comprehensive network data collection."""
        mock_run.side_effect = ["Interfaces", "Routes", "Netstat"]
        service = NetworkService()
        result = service.run()

        self.assertEqual(result["interfaces"], "Interfaces")
        self.assertEqual(result["routes"], "Routes")
        self.assertEqual(result["netstat"], "Netstat")
        self.assertEqual(mock_run.call_count, 3)
