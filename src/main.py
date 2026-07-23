"""
TDoc Platform Diagnostics - Main System Entry Gate
"""

import sys
from src.ui import ui_manager
from src.exceptions import TDocError, UIError
from src.router import TDocRouter
from src.services.factory import ServiceFactory


def main():
    """Initializes the security sandbox environment and hands off control to the HUD."""
    services = ServiceFactory.get_services()
    router = TDocRouter(services)
    utility_service = services.get("utility")
    try:
        ui_manager.start_hud(router, utility_service)
    except (UIError, TDocError) as e:
        print(f"FATAL SYSTEM ERROR DURING APPLICATION RUNTIME: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
