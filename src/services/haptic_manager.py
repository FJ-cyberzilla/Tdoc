"""
Haptic Manager Service - Encapsulates haptic feedback triggered by sensor anomalies.
"""

from typing import Any

from src.services.android.termux_api_service import TermuxApiService


class HapticManager:
    """Manages haptic alerts based on sensor intensity."""

    def __init__(self) -> None:
        self.api_service = TermuxApiService()
        self.enabled = True

    def toggle(self, enabled: bool) -> None:
        self.enabled = enabled

    def trigger_if_threshold_exceeded(self, data: dict[str, Any]) -> None:
        """Triggers haptic feedback if magnetic thresholds are met."""
        if not self.enabled:
            return

        mag = data.get("Magnetometer", {}).get("values")
        # Example threshold: If magnitude of magnetic field > 50
        if mag and sum(abs(v) for v in mag) > 50:
            self.api_service.trigger_haptic(duration_ms=200)
