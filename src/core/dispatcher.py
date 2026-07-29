"""
Command Dispatcher for Termux-Doctor.

Orchestrates user input mapping to actions and result handlers.
"""

from collections.abc import Callable
from typing import Any


class CommandDispatcher:
    """Dispatches user choices to appropriate handlers."""

    def __init__(self, router: Any, utility_service: Any):
        self.router = router
        self.utility_service = utility_service
        self.action_map: dict[str, tuple[str, Callable]] = {}

    def register_command(self, choice: str, action_name: str, handler: Callable):
        """Registers a command mapping."""
        self.action_map[choice] = (action_name, handler)

    def dispatch(self, choice: str) -> Any:
        """Dispatches the chosen action."""
        if choice not in self.action_map:
            raise ValueError(f"Invalid operation token: {choice}")

        action_name, handler = self.action_map[choice]

        if action_name in ["htop", "neofetch"]:
            return handler(None)

        result = self.router.route_action(action_name)
        return handler(result)
