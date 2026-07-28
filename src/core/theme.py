"""
Theme Manager - TDoc Design System & Telemetry HUD Engine.
Implements the 'Graphite & Plasma' aesthetic: minimalist greyscales
punctuated by high-contrast semantic accents for zero-fatigue monitoring.
"""

from rich.console import Console
from rich.theme import Theme

# Safely import external config, but we will wrap it in our modern design system
try:
    from src.constants import RICH_THEME_CONFIG
except ImportError:
    RICH_THEME_CONFIG: dict[str, str] = {}


class ThemeManager:
    """
    Centralized design system for TDoc.
    Manages typography, semantic thresholds, and terminal capability graceful degradation.
    """

    # ❖ THE GRAPHITE & PLASMA PALETTE (High-End Hex Colors)
    # Using hex codes allows Rich to render true 24-bit color on modern terminals,
    # while automatically degrading to 256-color palettes on older Termux setups.
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
        "navigation.active": "bold #10B981 on #064E3B",  # Emerald text on dark green bg (Pill effect)
        "navigation.inactive": "dim #71717A",
        "header.main": "bold #F8F9FA",  # High-contrast header text
        "error.text": "bold #FEF2F2 on #991B1B",  # High-contrast error badge
    }

    def __init__(self) -> None:
        """Initializes the layout engine and disables auto-highlighting for strict UI control."""
        self.theme = Theme(self.STYLES)

        # highlight=False is CRITICAL for modern UIs. It stops Rich from
        # arbitrarily turning numbers blue and brackets green.
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
            if value <= crit:
                return "status.critical"
            if value <= warn:
                return "status.warning"
            return "status.success"

        if value >= crit:
            return "status.critical"
        if value >= warn:
            return "status.warning"
        return "status.success"

    # =========================================================================
    # ❖ RAW ANSI INJECTION (Minimalist 256-Color Mapping)
    # For scripts or raw prints outside the Rich Console ecosystem.
    # =========================================================================

    @property
    def cyan(self) -> str:
        return "\033[38;5;45m"  # Plasma Cyan

    @property
    def slate(self) -> str:
        return "\033[38;5;246m"  # Crisp Slate Gray

    @property
    def muted(self) -> str:
        return "\033[38;5;240m"  # Deep Ash (For borders/dividers)

    @property
    def green(self) -> str:
        return "\033[38;5;40m"  # Clean Emerald

    @property
    def orange(self) -> str:
        return "\033[38;5;214m"  # Warm Amber

    @property
    def red(self) -> str:
        return "\033[38;5;196m"  # Sharp Red

    @property
    def reset(self) -> str:
        return "\033[0m"
