"""
Data models for security audit telemetry.
"""

from dataclasses import dataclass
from typing import cast


@dataclass
class SecurityAuditModel:
    root_state: str = "Not Rooted"
    selinux: str = "Enforcing"
    ld_preload: str = "Clean"
    suid_anomalies: int = 0

    @staticmethod
    def _get_safe_message(data: object, key: str, default: str) -> str:
        if isinstance(data, dict):
            # Safe because we verified it's a dict
            return str(cast(dict[str, object], data).get(key, default))
        return str(data)

    @staticmethod
    def _get_safe_int(value: object, default: int) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                pass
        return default

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SecurityAuditModel":
        if not isinstance(data, dict):
            return cls()

        return cls(
            root_state=cls._get_safe_message(data.get("root_presence", {}), "message", "Unknown"),
            selinux=str(data.get("selinux", "Enforcing")),
            ld_preload=cls._get_safe_message(data.get("ld_preload", {}), "message", "Clean"),
            suid_anomalies=cls._get_safe_int(data.get("termux_suid", 0), 0),
        )
