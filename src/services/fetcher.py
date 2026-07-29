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

        available = self._get_available_sensors()
        supported = [s for s in sensors if any(s in av for av in available)]
        unsupported = [s for s in sensors if s not in supported]

        data = {}
        # Mark unsupported sensors as 'NOT_DETECTED'
        for s in unsupported:
            data[s] = {"values": None, "status": "NOT_DETECTED"}

        if not supported:
            return data

        try:
            sensor_str = ",".join(supported)
            res = subprocess.run(
                ["termux-sensor", "-s", sensor_str, "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout.strip():
                actual_data = json.loads(res.stdout)
                data.update(actual_data)
        except Exception:
            pass
        return data

    def _get_mock_data(self, sensors: list[str]) -> dict[str, Any]:
        """Generates realistic mock data for sensors."""
        import random
        import time

        mock_data = {}
        t = time.time()
        for s in sensors:
            if "Accelerometer" in s:
                v = [random.uniform(-1, 1), random.uniform(-1, 1), 9.8 + random.uniform(-0.5, 0.5)]
                mock_data[s] = {"values": v}
            elif "Light" in s:
                mock_data[s] = {"values": [200.0 + 50 * random.uniform(-1, 1)]}
            elif "Barometer" in s:
                mock_data[s] = {"values": [1010.0 + random.uniform(-2, 2)]}
            elif "Step Counter" in s:
                mock_data[s] = {"values": [2500 + int(t % 100)]}
            elif "Gyroscope" in s:
                mock_data[s] = {"values": [random.uniform(-0.1, 0.1) for _ in range(3)]}
            else:
                mock_data[s] = {"values": [random.uniform(0, 100)]}
        return mock_data
