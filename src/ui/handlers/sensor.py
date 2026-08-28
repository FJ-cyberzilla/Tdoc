"""
Sensor Hub Handler - Manages live sensor telemetry updates and history.
"""

import asyncio
from typing import Any

from rich.live import Live

from src.router import TDocRouter
from src.ui.renderers.renderer import UIRenderer
from src.ui.renderers.sensor_renderer import SensorRenderer


class SensorHandler:
    """Handler for the Sensor Telemetry Hub view."""

    def __init__(self, renderer: UIRenderer, router: TDocRouter) -> None:
        self.main_renderer = renderer  # UIRenderer
        self.router = router
        self.sensor_renderer = SensorRenderer(renderer.console)
        self.history: dict[str, list[float]] = {
            "accel_mag": [],
            "light": [],
            "pressure": [],
        }
        self.max_history = 50

    async def handle(self, *args: Any, **kwargs: Any) -> None:
        """Runs the live sensor telemetry loop."""
        with Live(refresh_per_second=4, screen=True) as live:
            while True:
                # 1. Fetch sensor telemetry from router
                data = await self.router.get_sensor_hub_telemetry()

                # 2. Update history for graphs
                self._update_history(data)

                # 3. Render live view
                live.update(self.sensor_renderer.render_sensor_hub(data, self.history))

                # Sampling rate
                await asyncio.sleep(0.2)

    def _update_history(self, data: dict[str, Any]) -> None:
        """Updates internal history buffers for sparklines."""
        # Activity magnitude
        mag = float(data.get("activity", {}).get("magnitude", 0.0))
        self.history["accel_mag"].append(mag)

        # Light
        light = float(data.get("environment", {}).get("light", 0.0))
        self.history["light"].append(light)

        # Pressure
        pressure = float(data.get("environment", {}).get("pressure", 1013.25))
        self.history["pressure"].append(pressure)

        # Trim history
        for key in self.history:
            if len(self.history[key]) > self.max_history:
                self.history[key] = self.history[key][-self.max_history :]
