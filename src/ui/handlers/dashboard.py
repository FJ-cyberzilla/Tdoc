"""Handler for Telemetry Dashboard view."""

import time

from rich.live import Live


class DashboardHandler:
    def __init__(self, renderer, router):
        self.renderer = renderer
        self.router = router

    def handle(self, *args, **kwargs):
        # Check if user wants live mode (simplified for now: always live)
        with Live(refresh_per_second=0.5, screen=True) as live:
            while True:
                # 1. Gather raw telemetry
                env_raw = self.router.get_environment_telemetry()
                health_raw = self.router.get_health_telemetry()
                net_raw = self.router.get_network_telemetry()

                # 2. Render live
                live.update(
                    self.renderer.render_dashboard(
                        env_data=env_raw, net_data=net_raw, health_data=health_raw
                    )
                )
                time.sleep(2)
