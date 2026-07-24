"""
Theme Manager - Centralized styling definitions for Termux-Doctor.
"""

from rich.theme import Theme
from rich.console import Console
from src.constants import RICH_THEME_CONFIG


class ThemeManager:
    """Encapsulates all styling and theme definitions for TDoc."""

    # Theme definition for Rich, derived from TDoc constants
    STYLES = {
        "text.primary": RICH_THEME_CONFIG["text.primary"],
        "text.muted": RICH_THEME_CONFIG["text.muted"],
        "status.success": RICH_THEME_CONFIG["status.success"],
        "status.warning": RICH_THEME_CONFIG["status.warning"],
        "status.critical": RICH_THEME_CONFIG["status.critical"],
        "status.info": RICH_THEME_CONFIG["status.info"],
        "highlight": RICH_THEME_CONFIG["highlight"],
        "border.main": RICH_THEME_CONFIG["border.main"],
        "border.dashboard": RICH_THEME_CONFIG["border.dashboard"],
        "header.main": "bold #FF9100",
        "navigation.active": "bold green",
        "navigation.inactive": "dim white",
        "error.text": "bold red",
    }

    def __init__(self):
        self.theme = Theme(self.STYLES)
        self.console = Console(theme=self.theme)

    def get_status_style(self, value: float, warn: float, crit: float, reverse: bool = False) -> str:
        """Returns a semantic style based on value thresholds."""
        if reverse:
            if value >= crit:
                return "status.success"
            if value >= warn:
                return "status.warning"
            return "status.critical"
        else:
            if value >= crit:
                return "status.critical"
            if value >= warn:
                return "status.warning"
            return "status.success"

    @property
    def orange(self):
        return "\033[38;5;208m"

    @property
    def green(self):
        return "\033[32m"

    @property
    def red(self):
        return "\033[31m"

    @property
    def reset(self):
        return "\033[0m"
