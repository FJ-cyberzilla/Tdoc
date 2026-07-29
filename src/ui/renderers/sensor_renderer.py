"""
Sensor Hub Renderer - Aesthetic views and rich colored graphs for modular sensors.
"""

from typing import Any

from rich import box
from rich.panel import Panel
from rich.table import Table

from .visuals import GridBuilder, Visualizer


class SensorRenderer:
    """Handles rendering of the Sensor Hub with aesthetic graphs and stats."""

    def __init__(self, console):
        self.console = console
        self.grid_builder = GridBuilder()
        self.visualizer = Visualizer()
        self.blocks = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    def render_sensor_hub(self, data: dict[str, Any], history: dict[str, list[float]]) -> Panel:
        """Main entry point for rendering the Sensor Hub view."""
        master_grid = Table.grid(expand=True, padding=(0, 1))
        master_grid.add_column(ratio=1)
        master_grid.add_column(ratio=1)

        # Activity & Steps (Top Row)
        activity_panel = self._render_activity_card(
            data.get("activity", {}), history.get("accel_mag", []), data.get("orientation", {})
        )
        steps_panel = self._render_step_card(data.get("steps", {}))
        master_grid.add_row(activity_panel, steps_panel)

        # Environment & Security (Bottom Row)
        env_panel = self._render_env_card(
            data.get("environment", {}), history.get("light", []), history.get("pressure", [])
        )
        sec_panel = self._render_security_card(data.get("security", {}))
        master_grid.add_row(env_panel, sec_panel)

        return Panel(
            master_grid,
            title="[text.primary]SENSOR TELEMETRY HUB[/] [text.muted]• Cybertronic Matrix[/]",
            subtitle="[text.muted]Live Streaming Active[/]",
            box=box.ROUNDED,
            border_style="border.main",
            padding=(1, 2),
        )

    def _render_activity_card(
        self, activity: dict[str, Any], history: list[float], orientation: dict[str, Any] = None
    ) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)
        status = activity.get("status", "UNKNOWN")
        mag = activity.get("magnitude", 0.0)

        # State color
        color = (
            "green"
            if status == "STATIONARY"
            else "yellow"
            if status == "WALKING"
            else "red"
            if status == "RUNNING"
            else "white"
        )

        grid.add_row("STATE", f"[{color}]{status}[/]")
        grid.add_row("MAGNITUDE", f"{mag:.2f} m/s²")

        if orientation:
            rates = orientation.get("rotation_rates", [0.0, 0.0, 0.0])
            grid.add_row("GYRO (X,Y,Z)", f"{rates[0]:.2f}, {rates[1]:.2f}, {rates[2]:.2f}")

        graph = self._render_live_graph(history, color="cyan")
        grid.add_row("WAVEFORM", graph)

        return Panel(
            grid,
            title="[hud.label] ACTIVITY & ORIENTATION [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

    def _render_step_card(self, steps: dict[str, Any]) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)
        count = steps.get("count", 0)
        goal = steps.get("goal", 10000)
        progress = steps.get("progress", 0.0)

        bar = self.visualizer.render_capsule_bar(count, goal, width=15)
        grid.add_row("STEPS", f"[bold cyan]{count}[/] [text.muted]/ {goal}[/]")
        grid.add_row("GOAL", f"{progress:.1f}% {bar}")

        # Motivation
        msg = (
            "KEEP MOVING!" if progress < 50 else "HALF WAY!" if progress < 100 else "GOAL REACHED!"
        )
        grid.add_row("SYSTEM", f"[bold {('yellow' if progress < 100 else 'green')}]{msg}[/]")

        return Panel(
            grid,
            title="[hud.label] BIOMETRIC STEP TRACKER [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

    def _render_env_card(
        self, env: dict[str, Any], light_hist: list[float], press_hist: list[float]
    ) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)

        # Sensor statuses
        mag = env.get("Magnetometer", {})
        hall = env.get("Hall IC", {})

        def get_val_str(sensor_data):
            if sensor_data.get("status") == "NOT_DETECTED":
                return "[red]NOT DETECTED[/]"
            vals = sensor_data.get("values")
            return f"{vals[0]:.2f}" if vals else "[dim]--[/]"

        grid.add_row("LIGHT", f"{env.get('light', 0.0):.1f} lux")
        grid.add_row("GEOMAGNETIC", get_val_str(mag))
        grid.add_row("HALL SENSOR", get_val_str(hall))

        # Mini graphs
        l_graph = self._render_live_graph(light_hist, color="yellow", width=12)
        grid.add_row("LUMENS", l_graph)

        return Panel(
            grid,
            title="[hud.label] ENVIRONMENTAL SENSORS [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

    def _render_security_card(self, security: dict[str, Any]) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)

        state = security.get("lock_state", "UNKNOWN")
        avail = security.get("biometric_available", False)
        method = security.get("method", "N/A")

        badge = self.visualizer.render_state_badge(state, is_healthy=(state == "SECURE"))

        grid.add_row("LOCK STATE", badge)
        grid.add_row("BIOMETRIC", "[green]AVAIL[/]" if avail else "[red]ABSENT[/]")
        grid.add_row("PROTOCOL", f"[bold white]{method}[/]")
        grid.add_row("METHOD", "Hardware Cryptography")

        return Panel(
            grid,
            title="[hud.label] SECURITY INTERFACE [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

    def _render_live_graph(self, history: list[float], color: str = "cyan", width: int = 20) -> str:
        """Renders a simple colored sparkline graph using block characters."""
        if not history:
            return "[dim]-- NO DATA --[/]"

        # Take last 'width' elements
        data = history[-width:]
        if len(data) < width:
            data = [0.0] * (width - len(data)) + data

        min_v = min(data)
        max_v = max(data)
        rng = max_v - min_v
        if rng == 0:
            rng = 1

        spark = ""
        for v in data:
            idx = int(((v - min_v) / rng) * (len(self.blocks) - 1))
            spark += self.blocks[idx]

        return f"[{color}]{spark}[/{color}]"
