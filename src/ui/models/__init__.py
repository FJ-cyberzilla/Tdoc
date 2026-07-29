"""
UI Data Models for Termux-Doctor.
"""

from .hardware import BatteryModel, CPUModel, HardwareTelemetry, RAMModel
from .network import DNSModel, NetworkTelemetry, TelephonyModel, VPNModel
from .security import SecurityAuditModel

__all__ = [
    "CPUModel",
    "RAMModel",
    "BatteryModel",
    "HardwareTelemetry",
    "DNSModel",
    "VPNModel",
    "TelephonyModel",
    "NetworkTelemetry",
    "SecurityAuditModel",
]
