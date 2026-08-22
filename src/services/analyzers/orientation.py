from typing import Any

from src.interfaces import SensorAnalyzer


class OrientationAnalyzer(SensorAnalyzer):
    """Analyzes sensor data to detect device orientation/rotation using Gyroscope."""

    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        gyro = self._find_gyroscope(data)

        if not gyro:
            return {"status": "Unknown", "rotation_rates": [0.0, 0.0, 0.0]}

        rates = gyro.get("values", [0.0, 0.0, 0.0])
        return self._evaluate_rotation(rates)

    def _find_gyroscope(self, data: dict[str, Any]) -> Any:
        for key in data:
            if "Gyroscope" in key and "Uncalibrated" not in key:
                return data[key]
        return None

    def _evaluate_rotation(self, rates: list[float]) -> dict[str, Any]:
        is_rotating = any(abs(r) > 0.5 for r in rates)
        return {"status": "ROTATING" if is_rotating else "STABLE", "rotation_rates": rates}
