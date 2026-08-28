"""Handler for Network Deep-Dive view."""

from typing import Any

from src.router import TDocRouter
from src.ui.renderers.renderer import UIRenderer


class NetworkHandler:
    def __init__(self, renderer: UIRenderer, router: TDocRouter) -> None:
        self.renderer = renderer
        self.router = router

    async def handle(self, *args: Any, **kwargs: Any) -> None:
        net_raw = await self.router.get_network_telemetry()
        self.renderer.render_network_metrics(net_raw)
