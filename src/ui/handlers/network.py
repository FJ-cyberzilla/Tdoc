"""Handler for Network Deep-Dive view."""


class NetworkHandler:
    def __init__(self, renderer, router):
        self.renderer = renderer
        self.router = router

    def handle(self, *args, **kwargs):
        net_raw = self.router.get_network_telemetry()
        self.renderer.render_network_metrics(net_raw)
