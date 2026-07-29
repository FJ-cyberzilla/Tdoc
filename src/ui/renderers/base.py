from typing import Protocol

from rich.console import Console


class BaseRenderer(Protocol):
    """Protocol defining the interface for UI renderers."""

    def __init__(self, console: Console): ...

    def render(self, *args, **kwargs):
        """Renders the component."""
        ...
