"""
Grid layout builder for consistent terminal UI table formatting.
"""

from rich.table import Table


class GridBuilder:
    """Helper to build consistent, alignment-safe grids across all HUD cards."""

    @staticmethod
    def create_base_grid(
        label_width: int = 12, padding: tuple[int, int] = (0, 1), expand: bool = True
    ) -> Table:
        """
        Creates a standardized 2-column grid.

        Args:
            label_width: Width for the left-hand key column (default: 12).
            padding: Padding tuple (top/bottom, left/right).
            expand: Whether the grid fills available panel width.
        """
        grid = Table.grid(padding=padding, expand=expand)

        # Left column: Fixed label, right-aligned, strict no-wrap
        grid.add_column(style="hud.label", justify="right", width=label_width, no_wrap=True)

        # Right column: Value, left-aligned, safe ellipsis truncation
        grid.add_column(style="hud.value", justify="left", overflow="ellipsis")

        return grid

    @staticmethod
    def create_security_grid() -> Table:
        """Convenience method for wider labels in security audits."""
        return GridBuilder.create_base_grid(label_width=16)
