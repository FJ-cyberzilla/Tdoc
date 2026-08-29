from typing import Any, Protocol

from rich.table import Table


class RendererStrategy(Protocol):
    """Interface for rendering specific panels."""
    def render(self, data: Any) -> Table:
        ...
