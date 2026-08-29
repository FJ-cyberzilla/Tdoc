"""
Data models for network telemetry and cellular diagnostics.
"""

from dataclasses import dataclass, field
from typing import cast


@dataclass
class WifiModel:
    status: str = "ERROR"
    ssid: str = "N/A"
    ip: str = "N/A"
    rssi: str = "N/A"
    link_speed: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "WifiModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            status=str(data.get("status", "ERROR")),
            ssid=str(data.get("ssid", "N/A")),
            ip=str(data.get("ip", "N/A")),
            rssi=str(data.get("rssi", "N/A")),
            link_speed=str(data.get("link_speed_mbps", "N/A")),
        )


@dataclass
class SmsModel:
    total_messages: int = 0
    sent_recv_ratio: float = 0.0
    sender_diversity: float = 0.0
    peak_hour: int = 0
    domain_count: int = 0
    risky_domains: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SmsModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            total_messages=int(data.get("total_messages", 0)),
            sent_recv_ratio=float(data.get("sent_recv_ratio", 0.0)),
            sender_diversity=float(data.get("sender_diversity", 0.0)),
            peak_hour=int(data.get("peak_hour", 0)),
            domain_count=int(data.get("domain_count", 0)),
            risky_domains=list(cast(list[str], data.get("risky_domains", []))),
        )


@dataclass
class DeviceModel:
    carrier: str = "N/A"
    network_type: str = "N/A"
    data_state: str = "N/A"
    data_enabled: bool = False
    data_activity: str = "N/A"
    roaming: bool = False
    phone_type: str = "N/A"
    sim_state: str = "N/A"
    device_id: str = "N/A"
    sim_subscriber_id: str = "N/A"
    sim_serial_number: str = "N/A"

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DeviceModel":
        if not isinstance(data, dict):
            return cls()
        return cls(
            carrier=str(data.get("network_operator_name", "N/A")),
            network_type=str(data.get("network_type", "N/A")),
            data_state=str(data.get("data_state", "N/A")),
            data_enabled=bool(data.get("data_enabled", False)),
            data_activity=str(data.get("data_activity", "N/A")),
            roaming=bool(data.get("network_roaming", False)),
            phone_type=str(data.get("phone_type", "N/A")),
            sim_state=str(data.get("sim_state", "N/A")),
            device_id=str(data.get("device_id", "N/A")),
            sim_subscriber_id=str(data.get("sim_subscriber_id", "N/A")),
            sim_serial_number=str(data.get("sim_serial_number", "N/A")),
        )


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
    deviceinfo: DeviceModel = field(default_factory=DeviceModel)
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
            deviceinfo=DeviceModel.from_dict(device),
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
    wifi: WifiModel = field(default_factory=WifiModel)
    sms: SmsModel = field(default_factory=SmsModel)

    @classmethod
    def _get_dict(cls, data: dict[str, object], key: str) -> dict[str, object]:
        val = data.get(key)
        return cast(dict[str, object], val) if isinstance(val, dict) else {}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "NetworkTelemetry":
        if not isinstance(data, dict):
            return cls()

        topology = cls._get_dict(data, "topology")

        return cls(
            activity=str(data.get("activity", "idle")),
            local_ip=str(data.get("local_ip", "127.0.0.1")),
            fabric=str(topology.get("fabric", "CELLULAR")),
            hotspot_active=bool(data.get("hotspot_active", False)),
            dns=DNSModel.from_dict(cls._get_dict(data, "dns")),
            vpn=VPNModel.from_dict(cls._get_dict(data, "vpn")),
            telephony=TelephonyModel.from_dict(cls._get_dict(data, "telephony")),
            wifi=WifiModel.from_dict(cls._get_dict(data, "wifi")),
            sms=SmsModel.from_dict(cls._get_dict(data, "sms")),
        )
