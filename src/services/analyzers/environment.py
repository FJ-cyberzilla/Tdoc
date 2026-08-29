from typing import cast

from src.interfaces import SensorAnalyzer
from src.services.sensor_models import EnvironmentResult, SensorReading


class EnvironmentAnalyzer(SensorAnalyzer):
    """Analyzes sensor data for environmental monitoring (Barometer/Light)."""

    def _parse_light(self, val: dict[str, object]) -> float:
        values = cast(list[float], val.get("values", [50.0]))
        return float(values[0])

    def _parse_sensor_reading(self, val: dict[str, object]) -> SensorReading:
        return SensorReading(
            values=cast(list[float], val.get("values", [])),
            status=str(val.get("status", "UNKNOWN")),
        )

    def analyze(self, data: dict[str, object]) -> EnvironmentResult:
        light = 50.0
        magnetometer = None
        hall_ic = None

        for key, val in data.items():
            if not isinstance(val, dict):
                continue

            if "Light" in key:
                light = self._parse_light(val)
            elif "Magnetometer" in key:
                magnetometer = self._parse_sensor_reading(val)
            elif "Hall IC" in key:
                hall_ic = self._parse_sensor_reading(val)

        return EnvironmentResult(light=light, magnetometer=magnetometer, hall_ic=hall_ic)
