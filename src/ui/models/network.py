"""
Data models for network telemetry and cellular diagnostics.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DNSModel:
    servers: list[str] = field(default_factory=list)
    status: str = "OK"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DNSModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            servers=list(data.get("servers", [])),
            status=str(data.get("status", "OK")),
        )


@dataclass
class VPNModel:
    active: bool = False
    ip: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VPNModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            active=bool(data.get("active", False)),
            ip=str(data.get("ip", "N/A")),
        )


@dataclass
class TelephonyModel:
    carrier: str = "N/A"
    cell_type: str = "N/A"
    signal_dbm: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelephonyModel":
        if not isinstance(data, dict):
            return cls()

        device = data.get("deviceinfo", {})
        cell = data.get("cellinfo", [])
        if not isinstance(cell, list):
            cell = []
        sig = data.get("signalstrength", {})

        return cls(
            carrier=cls._parse_carrier(device),
            cell_type=cls._parse_cell_type(device, cell),
            signal_dbm=cls._parse_signal_dbm(sig, cell),
        )

    @staticmethod
    def _parse_carrier(device: dict[str, Any]) -> str:
        # Fallback sequence for carrier name
        fallback = ["network_operator_name", "sim_operator_name", "operator_name"]
        for key in fallback:
            if key in device:
                return str(device[key])

        if "error" in device:
            return "Access Denied"
        return "N/A"

    @staticmethod
    def _parse_cell_type(device: dict[str, Any], cell: list[dict[str, Any]]) -> str:
        if cell and (cell[0].get("type") or cell[0].get("network_type")):
            val = cell[0].get("type") or cell[0].get("network_type")
            return str(val).upper()

        if "phone_type" in device:
            return str(device["phone_type"]).upper()

        return "N/A"

    @staticmethod
    def _parse_signal_dbm(sig: dict[str, Any], cell: list[dict[str, Any]]) -> str:
        if "dbm" in sig:
            return f"{sig['dbm']} dBm"

        for entry in cell:
            dbm = entry.get("dbm") or entry.get("lte_rsrp")
            if dbm:
                return f"{dbm} dBm"
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
    def from_dict(cls, data: dict[str, Any]) -> "NetworkTelemetry":
        if not isinstance(data, dict):
            return cls()

        topology = data.get("topology", {})
        return cls(
            activity=str(data.get("activity", "idle")),
            local_ip=str(data.get("local_ip", "127.0.0.1")),
            fabric=str(topology.get("fabric", "CELLULAR")),
            hotspot_active=bool(data.get("hotspot_active", False)),
            dns=DNSModel.from_dict(data.get("dns", {})),
            vpn=VPNModel.from_dict(data.get("vpn", {})),
            telephony=TelephonyModel.from_dict(data.get("telephony", {})),
        )
