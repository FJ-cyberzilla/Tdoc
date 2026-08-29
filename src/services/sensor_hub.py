"""
Sensor Hub Service - Orchestrates modular sensor services with Termux:API.
"""

from src.interfaces import DiagnosticService, SensorFetcher
from src.services.analyzers.activity import ActivityAnalyzer
from src.services.analyzers.environment import EnvironmentAnalyzer
from src.services.analyzers.orientation import OrientationAnalyzer
from src.services.analyzers.steps import StepsAnalyzer
from src.services.haptic_manager import HapticManager
from src.services.sensor_models import (
    BiometricSecurityResult,
    SensorHubTelemetry,
)


class SensorHubService(DiagnosticService):
    """Orchestrates sensor data collection and modular analysis services."""

    def __init__(self, fetcher: SensorFetcher) -> None:
        self.fetcher = fetcher
        self.haptic_manager = HapticManager()
        self.analyzers = {
            "activity": ActivityAnalyzer(),
            "environment": EnvironmentAnalyzer(),
            "orientation": OrientationAnalyzer(),
            "steps": StepsAnalyzer(),
        }

    def set_haptic(self, enabled: bool):
        self.haptic_manager.toggle(enabled)

    def run(self) -> SensorHubTelemetry:
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

        # Run all analyzers
        activity = self.analyzers["activity"].analyze(data)
        environment = self.analyzers["environment"].analyze(data)
        orientation = self.analyzers["orientation"].analyze(data)
        steps = self.analyzers["steps"].analyze(data)

        # Add legacy/simple checks
        security = self.get_security_status()

        return SensorHubTelemetry(
            raw=data,
            activity=activity,  # type: ignore[arg-type] # This needs to be fixed in the protocol
            environment=environment,  # type: ignore[arg-type]
            orientation=orientation,  # type: ignore[arg-type]
            security=security,
            steps=steps,  # type: ignore[arg-type]
        )

    def get_security_status(self) -> BiometricSecurityResult:
        """Checks fingerprint sensor status for security."""
        import shutil

        has_auth = shutil.which("termux-fingerprint") is not None
        return BiometricSecurityResult(
            biometric_available=has_auth or not self.fetcher.supports_biometrics,
            lock_state="SECURE" if has_auth else "VULNERABLE",
            method="Fingerprint" if has_auth else "None",
        )
