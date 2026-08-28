"""
Unit tests for the TDocRouter.

This test suite covers route registration, resolution, middleware integration,
error handling, and route priorities.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.exceptions import RouterError
from src.interfaces import AsyncDiagnosticService, DiagnosticService
from src.router import TDocRouter


@pytest.mark.asyncio
async def test_route_registration_and_resolution():
    """Test that services can be registered and correctly resolved."""
    mock_service = AsyncMock(spec=AsyncDiagnosticService)
    mock_service.run.return_value = "Success"

    router = TDocRouter()
    router.register_service("test_service", mock_service)

    result = await router.route_action("test_service")
    assert result == "Success"
    mock_service.run.assert_called_once()


@pytest.mark.asyncio
async def test_error_handling_unknown_action():
    """Test that an unknown action ID raises a RouterError."""
    router = TDocRouter()
    with pytest.raises(RouterError, match="Unknown action ID"):
        await router.route_action("non_existent")


@pytest.mark.asyncio
async def test_error_handling_service_failure():
    """Test that a failing service raises a RouterError."""
    mock_service = AsyncMock(spec=AsyncDiagnosticService)
    mock_service.run.side_effect = Exception("Hardware failure")

    router = TDocRouter()
    router.register_service("fail_service", mock_service)

    with pytest.raises(RouterError, match="Error executing action 'fail_service'"):
        await router.route_action("fail_service")


@pytest.mark.asyncio
async def test_middleware_integration():
    """Test that middlewares are correctly applied in the routing pipeline."""
    mock_service = AsyncMock(spec=AsyncDiagnosticService)
    mock_service.run.return_value = "Result"

    router = TDocRouter()
    router.register_service("service", mock_service)

    # Async middleware that adds a prefix to the result
    async def prefix_middleware(action_id: str, next_handler: Any) -> Any:
        res = await next_handler(action_id)
        return f"Prefix: {res}"

    # Async middleware that logs the action
    async def logger_middleware(action_id: str, next_handler: Any) -> Any:
        res = await next_handler(action_id)
        return f"Logged({res})"

    router.add_middleware(prefix_middleware)
    router.add_middleware(logger_middleware)

    # Execution should be: prefix(logger(final())) -> Prefix: Logged(Result)
    # Because the first added middleware is the outermost in the chain.
    result = await router.route_action("service")
    assert result == "Prefix: Logged(Result)"


def test_route_priorities():
    """Test that route priorities are correctly stored."""
    mock_service = MagicMock(spec=DiagnosticService)
    router = TDocRouter()

    router.register_service("low", mock_service, priority=0)
    router.register_service("high", mock_service, priority=10)

    assert router.services["low"]["priority"] == 0
    assert router.services["high"]["priority"] == 10


@pytest.mark.asyncio
async def test_dashboard_composite_action():
    """Test that the dashboard action correctly aggregates results from multiple services."""
    mock_platform = AsyncMock(spec=AsyncDiagnosticService)
    mock_platform.run.return_value = "PlatformData"
    mock_network = AsyncMock(spec=AsyncDiagnosticService)
    mock_network.run.return_value = "NetworkData"
    mock_health = AsyncMock(spec=AsyncDiagnosticService)
    mock_health.run.return_value = "HealthData"

    router = TDocRouter({"platform": mock_platform, "network": mock_network, "health": mock_health})

    # Register dashboard composite action
    async def dashboard_action(r: TDocRouter) -> dict[str, Any]:
        return {
            "platform": await r.route_action("platform"),
            "network": await r.route_action("network"),
            "health": await r.route_action("health"),
        }

    router.register_composite_action("dashboard", dashboard_action)

    result = await router.route_action("dashboard")
    assert result["platform"] == "PlatformData"
    assert result["network"] == "NetworkData"
    assert result["health"] == "HealthData"
