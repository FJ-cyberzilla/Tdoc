from typing import Any

from src.interfaces import SensorAnalyzer


class EnvironmentAnalyzer(SensorAnalyzer):
    """Analyzes sensor data for environmental monitoring (Barometer/Light)."""

    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        result = {
            "light": 50.0,
            "Magnetometer": {"values": None, "status": "NOT_DETECTED"},
            "Hall IC": {"values": None, "status": "NOT_DETECTED"},
        }

        for key, val in data.items():
            if "Light" in key:
                result["light"] = val.get("values", [50.0])[0]
            if "Magnetometer" in key:
                result["Magnetometer"] = val
            if "Hall IC" in key:
                result["Hall IC"] = val

        return result
