from rich.table import Table


class GridBuilder:
    """Helper to build consistent grids."""

    @staticmethod
    def create_base_grid() -> Table:
        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="hud.label", justify="right", width=12)
        grid.add_column(style="hud.value")
        return grid
