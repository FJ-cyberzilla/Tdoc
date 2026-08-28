"""
Data models for network telemetry and cellular diagnostics.
"""

from dataclasses import dataclass, field
from typing import cast


@dataclass
class DNSModel:
    servers: list[str] = field(default_factory=list)
    status: str = "OK"

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DNSModel":
        if not isinstance(data, dict):
            return cls()

        servers = data.get("servers")
        status = data.get("status")

        return cls(
            servers=list(cast(list[str], servers)) if isinstance(servers, list) else [],
            status=str(status) if isinstance(status, str) else "OK",
        )


@dataclass
class VPNModel:
    active: bool = False
    ip: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "VPNModel":
        if not isinstance(data, dict):
            return cls()

        active = data.get("active")
        ip = data.get("ip")

        return cls(
            active=cast(bool, active) if isinstance(active, bool) else False,
            ip=str(ip) if isinstance(ip, str) else "N/A",
        )


@dataclass
class TelephonyModel:
    carrier: str = "N/A"
    cell_type: str = "N/A"
    signal_dbm: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "TelephonyModel":
        if not isinstance(data, dict):
            return cls()

        deviceinfo = data.get("deviceinfo")
        device = cast(dict[str, object], deviceinfo) if isinstance(deviceinfo, dict) else {}

        cellinfo = data.get("cellinfo")
        cell = cast(list[dict[str, object]], cellinfo) if isinstance(cellinfo, list) else []

        signalstrength = data.get("signalstrength")
        sig = cast(dict[str, object], signalstrength) if isinstance(signalstrength, dict) else {}

        return cls(
            carrier=cls._parse_carrier(device),
            cell_type=cls._parse_cell_type(device, cell),
            signal_dbm=cls._parse_signal_dbm(sig, cell),
        )

    @staticmethod
    def _parse_carrier(device: dict[str, object]) -> str:
        fallback = ["network_operator_name", "sim_operator_name", "operator_name"]
        for key in fallback:
            val = device.get(key)
            if val is not None:
                return str(val)

        if "error" in device:
            return "Access Denied"
        return "N/A"

    @staticmethod
    def _parse_cell_type(device: dict[str, object], cell: list[dict[str, object]]) -> str:
        if cell:
            first_cell = cell[0]
            val = first_cell.get("type") or first_cell.get("network_type")
            if val is not None:
                return str(val).upper()

        phone_type = device.get("phone_type")
        if phone_type is not None:
            return str(phone_type).upper()

        return "N/A"

    @staticmethod
    def _parse_signal_dbm(sig: dict[str, object], cell: list[dict[str, object]]) -> str:
        dbm = sig.get("dbm")
        if dbm is not None:
            return f"{dbm} dBm"

        for entry in cell:
            dbm_val = entry.get("dbm") or entry.get("lte_rsrp")
            if dbm_val is not None:
                return f"{dbm_val} dBm"
        return "N/A"


@dataclass
class NetworkTelemetry:
    activity: str = "idle"
    local_ip: str = "127.0.0.1"
    fabric: str = "CELLULAR"
    hotspot_active: bool = False
    dns: DNSModel = field(default_factory=DNSModel)
    vpn: VPNModel = field(default_factory=VPNModel)
    telephony: TelephonyModel = field(default_factory=TelephonyModel)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "NetworkTelemetry":
        if not isinstance(data, dict):
            return cls()

        topology_val = data.get("topology")
        topology = cast(dict[str, object], topology_val) if isinstance(topology_val, dict) else {}

        dns_val = data.get("dns")
        dns = cast(dict[str, object], dns_val) if isinstance(dns_val, dict) else {}

        vpn_val = data.get("vpn")
        vpn = cast(dict[str, object], vpn_val) if isinstance(vpn_val, dict) else {}

        telephony_val = data.get("telephony")
        telephony = (
            cast(dict[str, object], telephony_val) if isinstance(telephony_val, dict) else {}
        )

        return cls(
            activity=str(data.get("activity")) if isinstance(data.get("activity"), str) else "idle",
            local_ip=str(data.get("local_ip"))
            if isinstance(data.get("local_ip"), str)
            else "127.0.0.1",
            fabric=str(topology.get("fabric"))
            if isinstance(topology.get("fabric"), str)
            else "CELLULAR",
            hotspot_active=bool(data.get("hotspot_active"))
            if isinstance(data.get("hotspot_active"), bool)
            else False,
            dns=DNSModel.from_dict(dns),
            vpn=VPNModel.from_dict(vpn),
            telephony=TelephonyModel.from_dict(telephony),
        )
