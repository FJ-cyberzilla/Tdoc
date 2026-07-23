"""
Diagnostic service interface definitions.
"""

from typing import Protocol, Any


class DiagnosticService(Protocol):
    """Protocol defining the interface for diagnostic services."""

    def run(self) -> Any:
        """Executes the diagnostic check."""
