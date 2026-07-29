"""
Test suite for the UI Controller (HUDController).

This module verifies UI-related behaviors and initialization.
It focuses on setup and interaction with the router/dispatcher.
"""

from unittest.mock import MagicMock

from src.router import TDocRouter
from src.ui import HUDController


def test_hud_controller_initialization():
    """
    Verifies that HUDController initializes with the correct router and utility service.
    """
    mock_router = MagicMock(spec=TDocRouter)
    mock_utility = MagicMock()

    hud = HUDController(mock_router, mock_utility)

    assert hud.router == mock_router
    assert hud.utility_service == mock_utility
