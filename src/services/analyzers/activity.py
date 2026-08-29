from typing import cast

from src.interfaces import SensorAnalyzer
from src.services.sensor_models import ActivityResult


class ActivityAnalyzer(SensorAnalyzer):
    """Analyzes sensor data to detect activity (Walking, Running, Stationary)."""

    def _determine_activity(self, magnitude: float) -> str:
        """Determines activity status based on magnitude."""
        if magnitude > 15.0:
            return "RUNNING"
        if magnitude > 10.5:
            return "WALKING"
        if magnitude < 9.0:
            return "TILTED"
        return "STATIONARY"

    def analyze(self, data: dict[str, object]) -> ActivityResult:
        accel = next((data[key] for key in data if "Accelerometer" in key), None)

        if not isinstance(accel, dict):
            return ActivityResult(status="Unknown", magnitude=0.0, values=[0.0, 0.0, 0.0])

        # Calculate magnitude of acceleration
        vals = cast(list[float], accel.get("values", [0.0, 0.0, 0.0]))
        x, y, z = vals
        mag = (x**2 + y**2 + z**2) ** 0.5

        status = self._determine_activity(mag)
        return ActivityResult(status=status, magnitude=mag, values=[x, y, z])
