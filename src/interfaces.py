"""
Core diagnostic service interface definitions.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TelemetryService(Protocol):
    """Protocol for services that supply continuous metrics to the HUD."""

    def get_telemetry(self) -> dict[str, Any]:
        """Collects and returns structured telemetry data."""
        ...


@runtime_checkable
class DiagnosticService(Protocol):
    """Protocol defining the interface for diagnostic check and fix services."""

    def run(self) -> dict[str, Any]:
        """Executes the diagnostic check or remediation script."""
        ...


@runtime_checkable
class UtilityService(Protocol):
    """Protocol for external tool wrappers (e.g., htop, neofetch)."""

    def run_tool(self, tool_name: str) -> bool:
        """Executes a binary utility in the Termux shell environment."""
        ...


@runtime_checkable
class SensorFetcher(Protocol):
    """Protocol for fetching raw sensor data."""

    @property
    def supports_biometrics(self) -> bool:
        """Returns True if the fetcher supports biometric checks."""
        ...

    def get_data(self, sensors: list[str]) -> dict[str, Any]:
        """Fetches data from the specified sensors."""
        ...


@runtime_checkable
class SensorAnalyzer(Protocol):
    """Protocol for analyzing sensor data."""

    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        """Analyzes sensor data and returns insights."""
        ...
