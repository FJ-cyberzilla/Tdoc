"""Handler for Telemetry Dashboard view."""

import asyncio
from typing import Any

from rich.live import Live

from src.router import TDocRouter
from src.ui.models.hardware import HardwareTelemetry
from src.ui.models.network import NetworkTelemetry
from src.ui.renderers.renderer import UIRenderer


class DashboardHandler:
    def __init__(self, renderer: UIRenderer, router: TDocRouter) -> None:
        self.renderer = renderer
        self.router = router

    async def handle(self, *args: Any, **kwargs: Any) -> None:
        # Check if user wants live mode (simplified for now: always live)
        with Live(refresh_per_second=0.5, screen=True) as live:
            while True:
                # 1. Gather raw telemetry concurrently
                env_raw, health_raw, net_raw = await asyncio.gather(
                    self.router.get_environment_telemetry(),
                    self.router.get_health_telemetry(),
                    self.router.get_network_telemetry(),
                )

                hardware = HardwareTelemetry.from_dict(env_raw, health_raw)
                network = NetworkTelemetry.from_dict(net_raw)

                # 2. Render live
                live.update(
                    self.renderer.render_dashboard(
                        hardware=hardware, net_data=network
                    )
                )
                await asyncio.sleep(2)
