import json
import subprocess
from typing import Any


class SensorCollector:
    """Queries device sensor data."""

    def _list_sensors(self) -> list[str] | None:
        """Lists all sensors."""
        try:
            res = subprocess.run(["termux-sensor", "-l"], capture_output=True, text=True, timeout=2)
            if res.returncode != 0:
                return None
            return json.loads(res.stdout).get("sensors", [])
        except Exception:
            return None

    def _fetch_data(self, sensors: list[str]) -> dict[str, Any] | None:
        """Fetches data for specified sensors."""
        try:
            res = subprocess.run(
                ["termux-sensor", "-s", ",".join(sensors), "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout.strip():
                return json.loads(res.stdout)
            return None
        except Exception:
            return None

    def _is_relevant_sensor(self, sensor_name: str) -> bool:
        relevant_keywords = ["Accelerometer", "Light", "Magnetometer", "Gyroscope"]
        return any(keyword in sensor_name for keyword in relevant_keywords)

    def _filter_target_sensors(self, sensors: list[str]) -> list[str]:
        return [s for s in sensors if self._is_relevant_sensor(s)]

    def get_sensor_data(self) -> dict[str, Any]:
        """Queries device sensor data."""
        sensors = self._list_sensors()
        if sensors is None:
            return {"error": "Failed to list sensors"}

        target_sensors = self._filter_target_sensors(sensors)

        if not target_sensors:
            return {"error": "No relevant sensors found"}

        data = self._fetch_data(target_sensors)
        if data is None:
            return {"error": "Failed to fetch sensor data"}

        return data
