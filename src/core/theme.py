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
        "border.main": "#FF9100",
        "header.main": "bold #FF9100",
        "navigation.active": "bold green",
        "navigation.inactive": "dim white",
        "error.text": "bold red",
    }

    def __init__(self):
        self.theme = Theme(self.STYLES)
        self.console = Console(theme=self.theme)

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
