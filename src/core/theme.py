"""
Theme Manager - TDoc Design System & Telemetry HUD Engine.
Implements the 'Graphite & Plasma' aesthetic: minimalist greyscales
punctuated by high-contrast semantic accents for zero-fatigue monitoring.
"""

from rich.console import Console
from rich.theme import Theme

import src.constants

# Safely import external config, wrapped in our modern design system
RICH_THEME_CONFIG: dict[str, str] = getattr(src.constants, "RICH_THEME_CONFIG", {})


class ThemeManager:
    """
    Centralized design system for TDoc.
    Manages typography, semantic thresholds, and terminal capability graceful degradation.
    """

    STYLES: dict[str, str] = {
        # --- Typography & Hierarchy ---
        "text.primary": RICH_THEME_CONFIG.get("text.primary", "#F8F9FA"),  # Pristine White
        "text.secondary": "#A1A1AA",  # Zinc Slate
        "text.muted": RICH_THEME_CONFIG.get("text.muted", "dim #52525B"),  # Deep Ash
        # --- Plasma Accents (Interactive/Focus) ---
        "accent.primary": "bold #00E5FF",  # Electric Cyan
        "accent.secondary": "bold #B28DFF",  # Soft Plasma Purple
        # --- Structural Elements ---
        "border.main": RICH_THEME_CONFIG.get("border.main", "#27272A"),  # Barely-there Graphite
        "border.dashboard": RICH_THEME_CONFIG.get("border.dashboard", "#3F3F46"),  # Mid-tone Zinc
        "panel.bg": "on #18181B",  # Deepest Obsidian
        # --- Semantic Telemetry (The 'Dashboard' Feel) ---
        "status.success": RICH_THEME_CONFIG.get("status.success", "bold #10B981"),  # Emerald
        "status.warning": RICH_THEME_CONFIG.get("status.warning", "bold #F59E0B"),  # Amber
        "status.critical": RICH_THEME_CONFIG.get("status.critical", "bold #EF4444"),  # Rose Red
        "status.info": RICH_THEME_CONFIG.get("status.info", "#3B82F6"),  # Azure Blue
        # --- HUD Components ---
        "hud.label": "bold #71717A",  # Clean grey for metric names
        "hud.value": "bold #FFFFFF",  # Pure white for exact numbers
        "hud.unit": "dim #A1A1AA",  # Faded grey for % / MB / °C
        # --- Alerts & Navigation ---
        "navigation.active": "bold #10B981 on #064E3B",  # Emerald text on dark green bg
        "navigation.inactive": "dim #71717A",
        "header.main": "bold #F8F9FA",  # High-contrast header text
        "error.text": "bold #FEF2F2 on #991B1B",  # High-contrast error badge
    }

    def __init__(self) -> None:
        """Initializes the layout engine and disables auto-highlighting for strict UI control."""
        self.theme = Theme(self.STYLES)
        self.console = Console(theme=self.theme, highlight=False, soft_wrap=True)

    def get_status_style(
        self, value: float, warn: float, crit: float, reverse: bool = False
    ) -> str:
        """
        Calculates the semantic style for a telemetry metric.

        Args:
            value: The current sensor reading.
            warn: The warning threshold.
            crit: The critical threshold.
            reverse: If True, lower is worse (e.g., Battery, Available RAM).
                     If False, higher is worse (e.g., CPU Temp, Ping, Disk Space).
        """
        if reverse:
            return self._get_reverse_style(value, warn, crit)
        return self._get_standard_style(value, warn, crit)

    def _get_standard_style(self, value: float, warn: float, crit: float) -> str:
        if value >= crit:
            return "status.critical"
        if value >= warn:
            return "status.warning"
        return "status.success"

    def _get_reverse_style(self, value: float, warn: float, crit: float) -> str:
        if value <= crit:
            return "status.critical"
        if value <= warn:
            return "status.warning"
        return "status.success"

    def format_metric(
        self, value: float, unit: str, warn: float, crit: float, reverse: bool = False
    ) -> str:
        """Helper to return a styled metric reading with unit."""
        style = self.get_status_style(value, warn, crit, reverse=reverse)
        return f"[{style}]{value}[/][hud.unit]{unit}[/]"

    # --- RAW ANSI INJECTION (For direct terminal prints) ---
    @property
    def cyan(self) -> str:
        return "\033[38;5;45m"

    @property
    def slate(self) -> str:
        return "\033[38;5;246m"

    @property
    def muted(self) -> str:
        return "\033[38;5;240m"

    @property
    def green(self) -> str:
        return "\033[38;5;40m"

    @property
    def orange(self) -> str:
        return "\033[38;5;214m"

    @property
    def red(self) -> str:
        return "\033[38;5;196m"

    @property
    def reset(self) -> str:
        return "\033[0m"
