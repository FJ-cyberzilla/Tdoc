"""
Integration tests for the full system scan.

This test suite verifies the end-to-end functionality of the TDocRouter
when orchestrating multiple services for a dashboard request.
"""

from unittest.mock import MagicMock

from src.router import TDocRouter


def test_full_dashboard_scan():
    """
    Verify that the dashboard action correctly orchestrates platform,
    network, and health services.
    """
    mock_platform = MagicMock(spec=["run"])
    mock_platform.run.return_value = {"os": "android"}
    mock_network = MagicMock(spec=["run"])
    mock_network.run.return_value = {"status": "online"}
    mock_health = MagicMock(spec=["run"])
    mock_health.run.return_value = {"battery": "healthy"}

    router = TDocRouter({"platform": mock_platform, "network": mock_network, "health": mock_health})

    # Register dashboard composite action
    router.register_composite_action(
        "dashboard",
        lambda r: {
            "platform": r.route_action("platform"),
            "network": r.route_action("network"),
            "health": r.route_action("health"),
        },
    )

    # The dashboard action in TDocRouter triggers calls to all three services
    result = router.route_action("dashboard")

    assert result["platform"] == {"os": "android"}
    assert result["network"] == {"status": "online"}
    assert result["health"] == {"battery": "healthy"}

    mock_platform.run.assert_called_once()
    mock_network.run.assert_called_once()
    mock_health.run.assert_called_once()
