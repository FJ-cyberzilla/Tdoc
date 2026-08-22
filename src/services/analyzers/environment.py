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
            self._update_result_with_sensor(result, key, val)

        return result

    def _update_result_with_sensor(self, result: dict[str, Any], key: str, val: Any) -> None:
        if "Light" in key:
            result["light"] = val.get("values", [50.0])[0]
        elif "Magnetometer" in key:
            result["Magnetometer"] = val
        elif "Hall IC" in key:
            result["Hall IC"] = val
