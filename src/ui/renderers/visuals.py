"""
Visual elements, sparklines, and progress indicators for the Cybertronic UI.
"""

from rich.table import Table


class GridBuilder:
    """Helper to build consistent, alignment-safe grids."""

    @staticmethod
    def create_base_grid(label_width: int = 12) -> Table:
        """Creates a two-column grid with strict text bounds to prevent box overflow."""
        grid = Table.grid(padding=(0, 1), expand=True)
        grid.add_column(style="hud.label", justify="right", width=label_width, no_wrap=True)
        grid.add_column(style="hud.value", overflow="ellipsis")
        return grid


class Visualizer:
    """Handles high-density visual element rendering."""

    @staticmethod
    def braille_sparkline(data: list[float], width: int = 10) -> str:
        """Generates a Braille sparkline graph."""
        if not data:
            return "⠤" * width

        min_v, max_v = min(data), max(data)
        if min_v == max_v:
            return "⠤" * width

        normalized = [int((v - min_v) / (max_v - min_v) * 3) for v in data]
        chars = ["⠤", "⠔", "⠒", "⠢"]
        return "".join([chars[v] for v in normalized[:width]])

    @staticmethod
    def render_state_badge(text: str, is_healthy: bool = True) -> str:
        """Renders an inverted high-contrast status badge."""
        style = "[bold black on green]" if is_healthy else "[bold white on red]"
        return f"{style} ● {text.upper().strip()} [/]"

    @staticmethod
    def render_capsule_bar(used: float, total: float, width: int = 10) -> str:
        """Renders a color-graded block progress bar."""
        if total <= 0:
            return f"[dim]{'░' * width}[/dim] 0%"

        ratio = min(max(used / total, 0.0), 1.0)
        filled = int(ratio * width)
        empty = width - filled

        # Dynamic color based on usage
        if ratio < 0.70:
            color = "green"
        elif ratio < 0.85:
            color = "yellow"
        else:
            color = "red"

        return f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"

    @staticmethod
    def render_gradient_heatmap(temp: float) -> str:
        """Renders an ASCII density gradient heatmap based on temperature."""
        if temp < 35.0:
            return "[status.success]░░░░░░░░░░[/] [dim]Cool[/dim]"
        elif temp < 42.0:
            return "[status.info]░▒▓█░░░░░░[/] [cyan]Optimal[/cyan]"
        elif temp < 47.0:
            return "[status.warning]░▒▓████░░░[/] [yellow]Warm[/yellow]"
        else:
            return "[status.critical]██████████[/] [bold red]CRITICAL[/bold red]"

    @staticmethod
    def render_power_vector(wattage: float) -> str:
        """Renders power vector with directionality."""
        if wattage > 0.05:
            return f"[cyan]▲ +{wattage:.1f} W[/cyan]"
        elif wattage < -0.05:
            return f"[bold red]▼ {abs(wattage):.1f} W[/bold red]"
        return "[text.muted]◯ 0.0 W[/text.muted]"
