"""
Diagnostic service interface definitions.
"""

from typing import Any, Protocol


class DiagnosticService(Protocol):
    """Protocol defining the interface for diagnostic services."""

    def run(self) -> Any:
        """Executes the diagnostic check."""
