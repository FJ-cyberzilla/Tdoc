"""
TDoc Global Constants - Versioning & Engine Metadata
"""

__version__ = "1.2.0"
APP_NAME = "TDoc Platform Diagnostics"
CODENAME = "CYBER-MATRIX"
RICH_THEME_CONFIG = {
    "text.primary": "bold #FF9100",
    "text.muted": "dim #FF6D00",
    "status.success": "bold #00E676",
    "status.warning": "bold #FFEA00",
    "status.critical": "bold #FF1744",
    "status.info": "bold #2979FF",
    "highlight": "bold #AA00FF",
    "border.main": "#FF9100",
    "border.dashboard": "#00E676",
}
ANSI_ORANGE = "\033[38;5;208m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

HOME = "/data/data/com.termux/files/home"

SCAN_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 8080]

CHECK_SITES = [
    {"url": "https://google.com", "name": "Google", "type": "remote"},
    {"url": "http://127.0.0.1:8080", "name": "Local", "type": "local"},
]

SYSTEM_DEPENDENCIES = ["htop", "neofetch"]
