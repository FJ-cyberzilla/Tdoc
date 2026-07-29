"""
Centralized exception handling for the TDoc system.

Defines a hierarchy of custom exceptions to provide structured error reporting,
contextual metadata, and simplified error recovery across the application.
"""

from typing import Any


class TDocError(Exception):
    """
    Base exception for all TDoc-related errors.

    Attributes:
        message (str): A human-readable explanation of the error.
        context (dict[str, Any]): Additional diagnostic data related to the failure.
    """

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}


class NetworkError(TDocError):
    """Exception raised when a network-related operation fails."""


class SecurityError(TDocError):
    """Exception raised when a security audit fails or access is denied."""


class StorageError(TDocError):
    """Exception raised during file I/O operations."""


class ModuleError(TDocError):
    """Exception raised when a general module fails."""


class RouterError(TDocError):
    """Exception raised when the orchestrator fails to route a request."""


class UIError(TDocError):
    """Exception raised when the UI layer fails."""
