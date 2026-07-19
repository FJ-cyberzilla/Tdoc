"""
Centralized exception handling for the TDoc system.
"""

class TDocError(Exception):
    """Base exception for all TDoc-related errors."""
    pass

class ModuleError(TDocError):
    """Exception raised when a low-level module fails."""
    pass

class RouterError(TDocError):
    """Exception raised when the orchestrator fails to route a request."""
    pass

class UIError(TDocError):
    """Exception raised when the UI layer fails."""
    pass
