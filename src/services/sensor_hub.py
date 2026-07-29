"""
Sensor Hub Service - Orchestrates modular sensor services with Termux:API.
"""

from typing import Any

from src.interfaces import DiagnosticService, SensorAnalyzer, SensorFetcher
from src.services.analyzers.activity import ActivityAnalyzer
from src.services.analyzers.environment import EnvironmentAnalyzer
from src.services.analyzers.orientation import OrientationAnalyzer
from src.services.haptic_manager import HapticManager


class SensorHubService(DiagnosticService):
    """Orchestrates sensor data collection and modular analysis services."""

    def __init__(self, fetcher: SensorFetcher) -> None:
        self.fetcher = fetcher
        self.haptic_manager = HapticManager()
        self.analyzers: dict[str, SensorAnalyzer] = {
            "activity": ActivityAnalyzer(),
            "environment": EnvironmentAnalyzer(),
            "orientation": OrientationAnalyzer(),
        }

    def set_haptic(self, enabled: bool):
        self.haptic_manager.toggle(enabled)

    def run(self) -> dict[str, Any]:
        """Standard DiagnosticService entry point."""
        # Query a broader set of sensors
        sensors_to_query = [
            "Accelerometer",
            "Light",
            "Step Counter",
            "Gyroscope",
            "Magnetometer",
            "Hall IC",
        ]

        data = self.fetcher.get_data(sensors_to_query)

        # Trigger haptic alert
        self.haptic_manager.trigger_if_threshold_exceeded(data)

        results = {
            "raw": data,
        }

        # Run all analyzers
        for name, analyzer in self.analyzers.items():
            results[name] = analyzer.analyze(data)

        # Add legacy/simple checks
        results["security"] = self.get_security_status()

        return results

    def get_security_status(self) -> dict[str, Any]:
        """Checks fingerprint sensor status for security."""
        import shutil

        has_auth = shutil.which("termux-fingerprint") is not None
        return {
            "biometric_available": has_auth or not self.fetcher.supports_biometrics,
            "lock_state": "SECURE" if has_auth else "VULNERABLE",
            "method": "Fingerprint" if has_auth else "None",
        }
