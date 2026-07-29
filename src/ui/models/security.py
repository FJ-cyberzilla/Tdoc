"""
Data models for security audit telemetry.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class SecurityAuditModel:
    root_state: str = "Not Rooted"
    selinux: str = "Enforcing"
    ld_preload: str = "Clean"
    suid_anomalies: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SecurityAuditModel":
        if not isinstance(data, dict):
            return cls()

        root_info = data.get("root_presence", {})
        root_msg = (
            root_info.get("message", "Unknown") if isinstance(root_info, dict) else str(root_info)
        )

        ld_info = data.get("ld_preload", {})
        ld_msg = ld_info.get("message", "Clean") if isinstance(ld_info, dict) else str(ld_info)

        return cls(
            root_state=root_msg,
            selinux=str(data.get("selinux", "Enforcing")),
            ld_preload=ld_msg,
            suid_anomalies=int(data.get("termux_suid", 0)),
        )
