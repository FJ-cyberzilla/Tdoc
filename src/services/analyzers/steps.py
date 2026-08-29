from typing import cast

from src.interfaces import SensorAnalyzer
from src.services.sensor_models import StepsResult


class StepsAnalyzer(SensorAnalyzer):
    """Analyzes step counter data."""

    def analyze(self, data: dict[str, object]) -> StepsResult:
        step_data = next((data[key] for key in data if "Step Counter" in key), {})
        
        if not isinstance(step_data, dict):
            return StepsResult(count=0, goal=10000, progress=0.0)
            
        values = cast(list[float], step_data.get("values", [0.0]))
        count = int(values[0])
        goal = 10000
        progress = (count / goal) * 100

        return StepsResult(count=count, goal=goal, progress=progress)
