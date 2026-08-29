"""
Sensor Hub Renderer - Aesthetic views and rich colored graphs for modular sensors.
"""

from rich import box
from rich.panel import Panel
from rich.table import Table

from src.services.sensor_models import SensorHubTelemetry

from .visuals import (
    GridBuilder,
    HeatmapVisualizer,
    PowerVisualizer,
    ProgressVisualizer,
    SparklineVisualizer,
    StatusBadgeVisualizer,
)


class SensorRenderer:
    """Handles rendering of the Sensor Hub with aesthetic graphs and stats."""

    def __init__(self, console):
        self.console = console
        self.grid_builder = GridBuilder()
        self.sparkline = SparklineVisualizer()
        self.status_badge = StatusBadgeVisualizer()
        self.progress = ProgressVisualizer()
        self.heatmap = HeatmapVisualizer()
        self.power = PowerVisualizer()
        self.blocks = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    def render_sensor_hub(self, telemetry: SensorHubTelemetry, history: dict[str, list[float]]) -> Panel:
        """Main entry point for rendering the Sensor Hub view."""
        master_grid = Table.grid(expand=True, padding=(0, 1))
        master_grid.add_column(ratio=1)
        master_grid.add_column(ratio=1)

        # Activity & Steps (Top Row)
        activity_panel = self._render_activity_card(
            telemetry.activity, history.get("accel_mag", []), telemetry.orientation
        )
        steps_panel = self._render_step_card(telemetry.steps)
        master_grid.add_row(activity_panel, steps_panel)

        # Environment & Security (Bottom Row)
        env_panel = self._render_env_card(
            telemetry.environment, history.get("light", []), history.get("pressure", [])
        )
        sec_panel = self._render_security_card(telemetry.security)
        master_grid.add_row(env_panel, sec_panel)

        return Panel(
            master_grid,
            title="[text.primary]SENSOR TELEMETRY HUB[/] [text.muted]• Cybertronic Matrix[/]",
            subtitle="[text.muted]Live Streaming Active[/]",
            box=box.ROUNDED,
            border_style="border.main",
            padding=(1, 2),
        )

    def _render_activity_card(self, activity, history: list[float], orientation) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)
        
        self._add_activity_status_rows(grid, activity)

        if orientation:
            rates = orientation.rotation_rates
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

    def _add_activity_status_rows(self, grid: Table, activity) -> None:
        status = activity.status if activity else "UNKNOWN"
        mag = activity.magnitude if activity else 0.0
        color = self._get_activity_color(status)
        grid.add_row("STATE", f"[{color}]{status}[/]")
        grid.add_row("MAGNITUDE", f"{mag:.2f} m/s²")

    def _get_activity_color(self, status: str) -> str:
        if status == "STATIONARY":
            return "green"
        if status == "WALKING":
            return "yellow"
        if status == "RUNNING":
            return "red"
        return "white"

    def _render_step_card(self, steps) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)
        
        count = steps.count if steps else 0
        goal = steps.goal if steps else 10000
        progress = steps.progress if steps else 0.0

        bar = self.progress.render_capsule_bar(count, goal, width=15)
        grid.add_row("STEPS", f"[bold cyan]{count}[/] [text.muted]/ {goal}[/]")
        grid.add_row("GOAL", f"{progress:.1f}% {bar}")
        grid.add_row("SYSTEM", self._get_step_motivation_text(progress))

        return Panel(
            grid,
            title="[hud.label] BIOMETRIC STEP TRACKER [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

    def _get_step_motivation_text(self, progress: float) -> str:
        if progress < 50:
            msg, color = "KEEP MOVING!", "yellow"
        elif progress < 100:
            msg, color = "HALF WAY!", "yellow"
        else:
            msg, color = "GOAL REACHED!", "green"
        return f"[bold {color}]{msg}[/]"

    def _render_env_card(self, env, light_hist: list[float], press_hist: list[float]) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)

        def get_val_str(sensor_reading):
            if not sensor_reading or sensor_reading.status == "NOT_DETECTED":
                return "[red]NOT DETECTED[/]"
            vals = sensor_reading.values
            return f"{vals[0]:.2f}" if vals else "[dim]--[/]"

        grid.add_row("LIGHT", f"{env.light if env else 0.0:.1f} lux")
        grid.add_row("GEOMAGNETIC", get_val_str(env.magnetometer if env else None))
        grid.add_row("HALL SENSOR", get_val_str(env.hall_ic if env else None))

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

    def _render_security_card(self, security) -> Panel:
        grid = self.grid_builder.create_base_grid(label_width=14)

        state = security.lock_state if security else "UNKNOWN"
        avail = security.biometric_available if security else False
        method = security.method if security else "N/A"

        badge = self.status_badge.render(state, is_healthy=(state == "SECURE"))

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
