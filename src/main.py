"""
TDoc Platform Diagnostics - Main System Entry Gate
"""

import sys

from src.exceptions import TDocError, UIError
from src.router import TDocRouter
from src.services.factory import ServiceFactory
from src.ui import HUDController


def main():
    """Initializes the security sandbox environment and hands off control to the HUD."""
    services = ServiceFactory.get_services()
    router = TDocRouter(services)

    # Register composite actions
    router.register_composite_action(
        "dashboard",
        lambda r: {
            "platform": r.route_action("platform"),
            "network": r.route_action("network"),
            "health": r.route_action("health"),
        },
    )

    utility_service = services.get("utility")
    try:
        hud = HUDController(router, utility_service)
        hud.start()
    except (UIError, TDocError) as e:
        print(f"FATAL SYSTEM ERROR DURING APPLICATION RUNTIME: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
