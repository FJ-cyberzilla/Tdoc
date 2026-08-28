from typing import Protocol


class NetworkChecker(Protocol):
    """Protocol defining the interface for network diagnostic checkers."""

    def check(self) -> object:
        """Performs a network diagnostic check."""
        ...
