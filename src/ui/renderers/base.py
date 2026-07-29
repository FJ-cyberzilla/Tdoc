"""
Base protocols and interfaces for terminal UI renderers.
"""

from typing import Any, Protocol, runtime_checkable

from rich.console import Console


@runtime_checkable
class BaseRenderer(Protocol):
    """Protocol defining the contract for all UI renderers."""

    console: Console

    def __init__(self, console: Console) -> None: ...

    def render(self, *args: Any, **kwargs: Any) -> None:
        """Renders visual components directly to the console buffer."""
        ...
