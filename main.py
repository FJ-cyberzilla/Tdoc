"""
TDoc Platform Diagnostics - Main System Entry Gate
"""

import sys
import ui_manager
from router import TDocRouter
from advanced import environment, health, network, security
import updater

def main():
    """Initializes the security sandbox environment and hands off control to the HUD."""
    modules = {
        "environment": environment,
        "health": health,
        "network": network,
        "security": security,
        "updater": updater
    }
    router = TDocRouter(modules)
    try:
        ui_manager.start_hud(router)
    except Exception as e:
        print(f"FATAL SYSTEM ERROR DURING APPLICATION RUNTIME: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
