"""
Data models for hardware telemetry (CPU, RAM, Battery, Storage).
"""

from dataclasses import dataclass, field
from typing import cast


@dataclass
class CPUModel:
    model: str = "Android Processor"
    cores: int = 1
    frequency_mhz: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CPUModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            model=str(data.get("model", "Android Processor")),
            cores=int(cast(int, data.get("cores", 1))),
            frequency_mhz=float(cast(float, data.get("frequency_mhz", 0.0))),
        )


@dataclass
class RAMModel:
    used: float = 0.0
    total: float = 0.0

    @property
    def percentage(self) -> float:
        return (self.used / self.total * 100) if self.total > 0 else 0.0

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "RAMModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            used=float(cast(float, data.get("used", 0.0))),
            total=float(cast(float, data.get("total", 0.0))),
        )


@dataclass
class BatteryModel:
    percentage: int = 0
    capacity: str = "N/A"
    status: str = "DISCONNECTED"
    temp_num: float = 0.0
    wattage: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BatteryModel":
        if not isinstance(data, dict):
            return cls()

        raw_cap = data.get("capacity", data.get("percentage", "N/A"))
        cap_str = f"{raw_cap}%" if isinstance(raw_cap, (int, float)) else str(raw_cap)

        return cls(
            percentage=int(cast(int, data.get("percentage", 0))),
            capacity=cap_str,
            status=str(data.get("status", "DISCONNECTED")).upper(),
            temp_num=float(cast(float, data.get("temp_num", data.get("temperature", 0.0)))),
            wattage=float(cast(float, data.get("wattage", 0.0))),
        )


@dataclass
class HardwareTelemetry:
    cpu: CPUModel
    ram: RAMModel
    uptime: str = "N/A"
    used_storage_gb: float = 0.0
    total_storage_gb: float = 100.0
    battery: BatteryModel = field(default_factory=BatteryModel)

    @classmethod
    def from_dict(
        cls, env_data: dict[str, object], health_data: dict[str, object]
    ) -> "HardwareTelemetry":
        
        cpu_data = cast(dict[str, object], env_data.get("cpu", {}))
        ram_data = cast(dict[str, object], env_data.get("ram", {}))
        battery_data = cast(dict[str, object], health_data.get("battery", {}))
        
        return cls(
            cpu=CPUModel.from_dict(cpu_data if isinstance(cpu_data, dict) else {}),
            ram=RAMModel.from_dict(ram_data if isinstance(ram_data, dict) else {}),
            uptime=str(env_data.get("uptime", "N/A")),
            used_storage_gb=float(cast(float, health_data.get("used_storage_gb", 0.0))),
            total_storage_gb=float(cast(float, health_data.get("total_storage_gb", 100.0))),
            battery=BatteryModel.from_dict(battery_data),
        )
