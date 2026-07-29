from typing import Any, Protocol


class NetworkChecker(Protocol):
    """Protocol defining the interface for network diagnostic checkers."""

    def check(self) -> Any:
        """Performs a network diagnostic check."""
        ...
