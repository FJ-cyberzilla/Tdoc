import json
import shutil
import subprocess
from typing import Any

from src.interfaces import SensorFetcher


class TermuxSensorFetcher(SensorFetcher):
    """Fetches raw sensor data using termux-sensor."""

    def __init__(self) -> None:
        self.is_android = bool(shutil.which("termux-sensor"))

    @property
    def supports_biometrics(self) -> bool:
        """Returns True if the fetcher supports biometric checks."""
        return self.is_android

    def _get_available_sensors(self) -> list[str]:
        """Returns a list of actually available sensors."""
        if not self.is_android:
            return []

        try:
            res = subprocess.run(
                ["termux-sensor", "-l"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                data = json.loads(res.stdout)
                return data.get("sensors", [])
        except Exception:
            pass
        return []

    def get_data(self, sensors: list[str]) -> dict[str, Any]:
        if not self.is_android:
            return self._get_mock_data(sensors)

        supported, data = self._process_sensor_availability(sensors)

        if supported:
            actual_data = self._execute_sensor_command(supported)
            data.update(actual_data)
        
        return data

    def _process_sensor_availability(self, sensors: list[str]) -> tuple[list[str], dict[str, Any]]:
        available = self._get_available_sensors()
        supported = self._get_supported_sensors(sensors, available)
        unsupported = self._get_unsupported_sensors(sensors, supported)

        data = self._create_unsupported_data(unsupported)
        return supported, data

    def _get_supported_sensors(self, sensors: list[str], available: list[str]) -> list[str]:
        return [s for s in sensors if any(s in av for av in available)]

    def _get_unsupported_sensors(self, sensors: list[str], supported: list[str]) -> list[str]:
        return [s for s in sensors if s not in supported]

    def _create_unsupported_data(self, unsupported: list[str]) -> dict[str, Any]:
        return {s: {"values": None, "status": "NOT_DETECTED"} for s in unsupported}

    def _execute_sensor_command(self, supported: list[str]) -> dict[str, Any]:
        try:
            sensor_str = ",".join(supported)
            res = subprocess.run(
                ["termux-sensor", "-s", sensor_str, "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout.strip():
                return json.loads(res.stdout)
        except Exception:
            pass
        return {}

    def _get_mock_data(self, sensors: list[str]) -> dict[str, Any]:
        """Generates realistic mock data for sensors."""
        import random
        import time

        mock_data = {}
        t = time.time()
        for s in sensors:
            mock_data[s] = {"values": self._get_sensor_mock_values(s, t)}
        return mock_data

    def _get_sensor_mock_values(self, s: str, t: float) -> list[float]:
        import random
        if "Accelerometer" in s:
            return [random.uniform(-1, 1), random.uniform(-1, 1), 9.8 + random.uniform(-0.5, 0.5)]
        elif "Light" in s:
            return [200.0 + 50 * random.uniform(-1, 1)]
        elif "Barometer" in s:
            return [1010.0 + random.uniform(-2, 2)]
        elif "Step Counter" in s:
            return [2500 + int(t % 100)]
        elif "Gyroscope" in s:
            return [random.uniform(-0.1, 0.1) for _ in range(3)]
        return [random.uniform(0, 100)]
