import json
import subprocess
from typing import Any


class SensorCollector:
    """Queries device sensor data."""

    def get_sensor_data(self) -> dict[str, Any]:
        try:
            # Get list of all sensors
            res_list = subprocess.run(
                ["termux-sensor", "-l"], capture_output=True, text=True, timeout=2
            )
            if res_list.returncode != 0:
                return {"error": "Failed to list sensors"}

            sensors = json.loads(res_list.stdout).get("sensors", [])

            # Sample relevant sensors
            relevant_keywords = ["Accelerometer", "Light", "Magnetometer", "Gyroscope"]
            target_sensors = [s for s in sensors if any(k in s for k in relevant_keywords)]

            # Fetch data for selected sensors
            res_data = subprocess.run(
                ["termux-sensor", "-s", ",".join(target_sensors), "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if res_data.returncode == 0 and res_data.stdout.strip():
                return json.loads(res_data.stdout)
            return {"error": "Failed to fetch sensor data"}
        except Exception:
            return {"error": "Sensor access error"}
