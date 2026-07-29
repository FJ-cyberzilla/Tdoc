"""
Unit tests for the TDocRouter.

This test suite covers route registration, resolution, middleware integration,
error handling, and route priorities.
"""

from unittest.mock import MagicMock

import pytest

from src.exceptions import RouterError
from src.interfaces import DiagnosticService
from src.router import TDocRouter


def test_route_registration_and_resolution():
    """Test that services can be registered and correctly resolved."""
    mock_service = MagicMock(spec=DiagnosticService)
    mock_service.run.return_value = "Success"

    router = TDocRouter()
    router.register_service("test_service", mock_service)

    result = router.route_action("test_service")
    assert result == "Success"
    mock_service.run.assert_called_once()


def test_error_handling_unknown_action():
    """Test that an unknown action ID raises a RouterError."""
    router = TDocRouter()
    with pytest.raises(RouterError, match="Unknown action ID"):
        router.route_action("non_existent")


def test_error_handling_service_failure():
    """Test that a failing service raises a RouterError."""
    mock_service = MagicMock(spec=DiagnosticService)
    mock_service.run.side_effect = Exception("Hardware failure")

    router = TDocRouter()
    router.register_service("fail_service", mock_service)

    with pytest.raises(RouterError, match="Error executing action 'fail_service'"):
        router.route_action("fail_service")


def test_middleware_integration():
    """Test that middlewares are correctly applied in the routing pipeline."""
    mock_service = MagicMock(spec=DiagnosticService)
    mock_service.run.return_value = "Result"

    router = TDocRouter()
    router.register_service("service", mock_service)

    # Middleware that adds a prefix to the result
    def prefix_middleware(action_id, next_handler):
        res = next_handler(action_id)
        return f"Prefix: {res}"

    # Middleware that logs the action (here it just changes the result again)
    def logger_middleware(action_id, next_handler):
        res = next_handler(action_id)
        return f"Logged({res})"

    router.add_middleware(prefix_middleware)
    router.add_middleware(logger_middleware)

    # Execution should be: prefix(logger(final())) -> Prefix: Logged(Result)
    # Because the first added middleware is the outermost in the chain.
    result = router.route_action("service")
    assert result == "Prefix: Logged(Result)"


def test_route_priorities():
    """Test that route priorities are correctly stored."""
    mock_service = MagicMock(spec=DiagnosticService)
    router = TDocRouter()

    router.register_service("low", mock_service, priority=0)
    router.register_service("high", mock_service, priority=10)

    assert router.services["low"]["priority"] == 0
    assert router.services["high"]["priority"] == 10


def test_dashboard_composite_action():
    """Test that the dashboard action correctly aggregates results from multiple services."""
    mock_platform = MagicMock(spec=DiagnosticService)
    mock_platform.run.return_value = "PlatformData"
    mock_network = MagicMock(spec=DiagnosticService)
    mock_network.run.return_value = "NetworkData"
    mock_health = MagicMock(spec=DiagnosticService)
    mock_health.run.return_value = "HealthData"

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

    result = router.route_action("dashboard")
    assert result["platform"] == "PlatformData"
    assert result["network"] == "NetworkData"
    assert result["health"] == "HealthData"
