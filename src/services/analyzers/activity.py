from typing import Any

from src.interfaces import SensorAnalyzer


class ActivityAnalyzer(SensorAnalyzer):
    """Analyzes sensor data to detect activity (Walking, Running, Stationary)."""

    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        accel = None
        for key in data:
            if "Accelerometer" in key:
                accel = data[key]
                break

        if not accel:
            return {"status": "Unknown", "magnitude": 0.0}

        # Calculate magnitude of acceleration
        x, y, z = accel.get("values", [0.0, 0.0, 0.0])
        mag = (x**2 + y**2 + z**2) ** 0.5

        # Simple threshold-based activity detection
        if mag > 15.0:
            status = "RUNNING"
        elif mag > 10.5:
            status = "WALKING"
        elif mag < 9.0:
            status = "TILTED"
        else:
            status = "STATIONARY"

        return {"status": status, "magnitude": mag, "values": [x, y, z]}
