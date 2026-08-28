import pytest
from unittest.mock import MagicMock, patch

from src.router import TDocRouter
from src.ui import HUDController


@pytest.mark.asyncio
async def test_ui_hud_start():
    """Verify that HUDController correctly interacts with the router."""
    mock_router = MagicMock(spec=TDocRouter)
    mock_utility = MagicMock()

    # Mock to prevent actual UI loop from running
    with patch.object(HUDController, "start") as mock_start:
        hud = HUDController(mock_router, mock_utility)
        await hud.start()

        mock_start.assert_called_once()
