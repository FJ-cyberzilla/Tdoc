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

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SecurityAuditModel":
        if not isinstance(data, dict):
            return cls()

        root_info: object = data.get("root_presence", {})

        # Ensure root_info is handled safely
        root_msg: str
        if isinstance(root_info, dict):
            # Casting to dict[str, object] because we checked it's a dict
            root_dict = cast(dict[str, object], root_info)
            root_msg = str(root_dict.get("message", "Unknown"))
        else:
            root_msg = str(root_info)

        ld_info: object = data.get("ld_preload", {})

        # Ensure ld_info is handled safely
        ld_msg: str
        if isinstance(ld_info, dict):
            # Casting to dict[str, object] because we checked it's a dict
            ld_dict = cast(dict[str, object], ld_info)
            ld_msg = str(ld_dict.get("message", "Clean"))
        else:
            ld_msg = str(ld_info)

        selinux_val = data.get("selinux", "Enforcing")

        # Handle potential suid_anomalies
        suid_val = data.get("termux_suid", 0)
        suid_int: int = 0
        if isinstance(suid_val, int):
            suid_int = suid_val
        elif isinstance(suid_val, str):
            try:
                suid_int = int(suid_val)
            except ValueError:
                suid_int = 0

        return cls(
            root_state=root_msg,
            selinux=str(selinux_val),
            ld_preload=ld_msg,
            suid_anomalies=suid_int,
        )
