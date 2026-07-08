"""
TDoc Platform Diagnostics - Main System Entry Gate
"""

import sys
import manager


def main():
    """Initializes the security sandbox environment and hands off control to the HUD."""
    try:
        manager.start_hud_router()
    except Exception as e:
        print(f"FATAL SYSTEM ERROR DURING APPLICATION RUNTIME: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
