from typing import Any

from src.interfaces import SensorAnalyzer


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

    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        accel = next((data[key] for key in data if "Accelerometer" in key), None)

        if not accel:
            return {"status": "Unknown", "magnitude": 0.0}

        # Calculate magnitude of acceleration
        x, y, z = accel.get("values", [0.0, 0.0, 0.0])
        mag = (x**2 + y**2 + z**2) ** 0.5

        status = self._determine_activity(mag)
        return {"status": status, "magnitude": mag, "values": [x, y, z]}
