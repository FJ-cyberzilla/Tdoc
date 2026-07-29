"""
Sensor Hub Handler - Manages live sensor telemetry updates and history.
"""

import time

from rich.live import Live

from src.ui.renderers.sensor_renderer import SensorRenderer


class SensorHandler:
    """Handler for the Sensor Telemetry Hub view."""

    def __init__(self, renderer, router):
        self.main_renderer = renderer  # UIRenderer
        self.router = router
        self.sensor_renderer = SensorRenderer(renderer.console)
        self.history = {"accel_mag": [], "light": [], "pressure": []}
        self.max_history = 50

    def handle(self, *args, **kwargs):
        """Runs the live sensor telemetry loop."""
        with Live(refresh_per_second=4, screen=True) as live:
            try:
                while True:
                    # 1. Fetch sensor telemetry from router
                    data = self.router.get_sensor_hub_telemetry()

                    # 2. Update history for graphs
                    self._update_history(data)

                    # 3. Render live view
                    live.update(self.sensor_renderer.render_sensor_hub(data, self.history))

                    # Sampling rate
                    time.sleep(0.2)
            except KeyboardInterrupt:
                pass

    def _update_history(self, data: dict):
        """Updates internal history buffers for sparklines."""
        # Activity magnitude
        mag = data.get("activity", {}).get("magnitude", 0.0)
        self.history["accel_mag"].append(mag)

        # Light
        light = data.get("environment", {}).get("light", 0.0)
        self.history["light"].append(light)

        # Pressure
        pressure = data.get("environment", {}).get("pressure", 1013.25)
        self.history["pressure"].append(pressure)

        # Trim history
        for key in self.history:
            if len(self.history[key]) > self.max_history:
                self.history[key] = self.history[key][-self.max_history :]
