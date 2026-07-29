class Visualizer:
    """Handles visual element rendering (sparklines, gradients)."""

    @staticmethod
    def braille_sparkline(data: list[float], width: int = 10) -> str:
        """Generates a Braille sparkline graph."""
        if not data:
            return "⠤" * width

        # Simple normalization to Braille range (0-3)
        min_v, max_v = min(data), max(data)
        if min_v == max_v:
            return "⠤" * width

        normalized = [int((v - min_v) / (max_v - min_v) * 3) for v in data]

        # Braille dots: ⠤, ⠔, ⠒, ⠢
        chars = ["⠤", "⠔", "⠒", "⠢"]
        return "".join([chars[v] for v in normalized[:width]])

    @staticmethod
    def render_state_badge(text: str, is_healthy: bool = True) -> str:
        """Renders an inverted high-contrast status badge."""
        style = "[bold white on green]" if is_healthy else "[bold white on red]"
        return f"{style} ● {text.upper()} [/]"

    @staticmethod
    def render_gradient_heatmap(temp: float) -> str:
        """Renders an ASCII density gradient heatmap based on temperature."""
        if temp < 35:
            return "[status.success]░░░░░░░░░░[/] Cool"
        elif temp < 42:
            return "[status.info]░▒▓█░░░░░░[/] Optimal"
        elif temp < 47:
            return "[status.warning]░▒▓████░░░[/] Warm"
        else:
            return "[status.critical]██████████[/] CRITICAL"

    @staticmethod
    def render_power_vector(wattage: float) -> str:
        """Renders power vector with directionality."""
        if wattage > 0:
            return f"[cyan]▲ +{wattage:.1f} W[/]"
        elif wattage < 0:
            return f"[red]▼ {wattage:.1f} W[/]"
        return f"[white]◯ {wattage:.1f} W[/]"
