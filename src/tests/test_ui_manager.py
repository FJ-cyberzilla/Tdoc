from unittest.mock import MagicMock

from src.router import TDocRouter
from src.ui.ui_manager import HUDLoop


def test_hud_loop_initialization():
    mock_router = MagicMock(spec=TDocRouter)
    mock_utility = MagicMock()

    hud = HUDLoop(mock_router, mock_utility)

    assert hud.router == mock_router
    assert hud.utility_service == mock_utility


# Note: Testing the start() method is difficult because of the infinite loop.
# I will need to refactor the loop slightly to be testable (e.g., accepting an input stream or limit)
# during the refactoring process.
