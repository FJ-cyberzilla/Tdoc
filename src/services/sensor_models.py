"""
Typed data models for sensor telemetry.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BiometricSecurityResult:
    biometric_available: bool
    lock_state: str
    method: str


@dataclass(frozen=True)
class ActivityResult:
    status: str
    magnitude: float
    values: list[float]


@dataclass(frozen=True)
class SensorReading:
    values: list[float] | None
    status: str


@dataclass(frozen=True)
class EnvironmentResult:
    light: float
    magnetometer: SensorReading | None
    hall_ic: SensorReading | None


@dataclass(frozen=True)
class OrientationResult:
    status: str
    rotation_rates: list[float]


@dataclass(frozen=True)
class StepsResult:
    count: int
    goal: int
    progress: float


@dataclass(frozen=True)
class SensorHubTelemetry:
    raw: dict[str, object]
    activity: ActivityResult | None
    environment: EnvironmentResult | None
    orientation: OrientationResult | None
    security: BiometricSecurityResult | None
    steps: StepsResult | None
