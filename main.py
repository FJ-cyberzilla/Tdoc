"""
TDoc Command Center - Core Application Launcher
"""

import sys

# Safety verification to ensure execution is containerized or package-relative
if sys.version_info < (3, 7):
    print("CRITICAL ERROR: TDoc requires Python 3.7+ features for subprocess management.")
    sys.exit(1)

try:
    import manager
except ImportError:
    # Handles direct execution gracefully if not called as a module flag
    import manager

def run_system_main() -> None:
    """Initializes environment bindings and transfers execution control to the HUD."""
    try:
        manager.launch_interface_loop()
    except Exception as fatal_err:
        print(f"FATAL SYSTEM ERROR DURING APPLICATION RUNTIME: {fatal_err}")
        sys.exit(1)

if __name__ == "__main__":
    run_system_main()
