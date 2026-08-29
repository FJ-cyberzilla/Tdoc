"""
UI Views and dashboard layout renderers for Termux-Doctor console interface.
"""

import os
from typing import cast

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.constants import __version__
from src.ui.models.hardware import HardwareTelemetry
from src.ui.models.network import (
    DeviceModel,
    DNSModel,
    NetworkTelemetry,
    SmsModel,
    TelephonyModel,
    WifiModel,
)
from src.ui.models.security import SecurityAuditModel

from .visuals import (
    GridBuilder,
    HeatmapVisualizer,
    PowerVisualizer,
    ProgressVisualizer,
    SparklineVisualizer,
    StatusBadgeVisualizer,
)


class UIRenderer:
    """Handles rendering of high-density, modern terminal UI components."""

    def __init__(self, console):
        self.console = console
        self.grid_builder = GridBuilder()
        self.sparkline = SparklineVisualizer()
        self.status_badge = StatusBadgeVisualizer()
        self.progress = ProgressVisualizer()
        self.heatmap = HeatmapVisualizer()
        self.power = PowerVisualizer()

    def clear_screen(self):
        """Wipes terminal view buffer."""
        os.system("clear" if os.name != "nt" else "cls")

    def render_header(self):
        """Renders the sleek top branding banner."""
        header = Table.grid(padding=(0, 1), expand=True)
        header.add_column(justify="left", ratio=1)
        header.add_column(justify="right")
        header.add_row(
            "[accent.primary]⚡ T-DOC[/] [text.muted]::[/] [text.primary]FJ™ Cybertronic[/]",
            f"[text.muted]v{__version__}[/]",
        )
        self.console.print(
            Panel(header, box=box.ROUNDED, border_style="border.main", padding=(0, 2))
        )

    def render_navigation(self):
        """Renders the navigation menu."""
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2), expand=True)
        table.add_column("Key", style="accent.secondary", justify="right", width=4)
        table.add_column("Action", style="text.primary")
        table.add_column("Module", style="text.muted")

        menu_items = [
            ("1", "Telemetry Dashboard", "• Hardware, HDD, Env"),
            ("2", "Network Deep-Dive", "• DNS Leak, Latency, Hotspot"),
            ("3", "Security Audit", "• SUID, Root, SELinux"),
            ("4", "Workspace Status", "• Git Status, Sync"),
            ("5", "Package Manager", "• Installed Packages"),
            ("6", "Run Htop", "• Process Monitor"),
            ("7", "Run Neofetch", "• System Info"),
            ("8", "Sensor Hub", "• Live Graph & Activity"),
            ("0", "Exit System", ""),
        ]

        for key, action, module in menu_items:
            table.add_row(key, action, module)

        self.console.print(
            Panel(
                table,
                title="[hud.label] NAVIGATION MATRIX [/]",
                title_align="left",
                border_style="border.main",
                box=box.ROUNDED,
            )
        )

    def render_dashboard(
        self, hardware: HardwareTelemetry, net_data: NetworkTelemetry
    ) -> Panel:
        """Constructs and returns the dashboard panel for live updates."""

        # Build cards
        env_panel = Panel(
            self._build_env_grid(hardware),
            title="[hud.label] SYSTEM HARDWARE [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

        health_panel = Panel(
            self._build_health_grid(hardware),
            title="[hud.label] STORAGE & POWER [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

        net_panel = Panel(
            self._build_net_grid(net_data),
            title="[hud.label] NETWORK FABRIC [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
            expand=True,
        )

        # Left Column Stack
        left_stack = Table.grid(expand=True)
        left_stack.add_row(env_panel)
        left_stack.add_row(health_panel)

        # Right Column Stack
        right_stack = Table.grid(expand=True)
        right_stack.add_row(net_panel)

        # Master 2-Column Side-by-Side Layout
        master_grid = Table.grid(expand=True, padding=(0, 1))
        master_grid.add_column(ratio=1)
        master_grid.add_column(ratio=1)
        master_grid.add_row(left_stack, right_stack)

        return Panel(
            master_grid,
            title="[text.primary]LIVE TELEMETRY[/] [text.muted]• Cybertronic Systems[/]",
            box=box.ROUNDED,
            border_style="border.main",
        )

    def _build_env_grid(self, hardware: HardwareTelemetry) -> Table:
        grid = self.grid_builder.create_base_grid()
        
        grid.add_row(
            "CPU", f"{hardware.cpu.model} [text.muted]({hardware.cpu.cores} cores)[/]"
        )
        grid.add_row(
            "RAM",
            f"{hardware.ram.used:.1f} GB [text.muted]/[/] {hardware.ram.total:.1f} GB",
        )
        grid.add_row("UPTIME", f"{hardware.uptime}")
        return grid

    def _build_net_grid(self, net_data: NetworkTelemetry) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Network Activity
        activity = net_data.activity
        glyph = self.get_activity_glyph(activity)
        grid.add_row("FABRIC", f"{glyph} {activity.upper()}")
        grid.add_row("LOCAL IP", net_data.local_ip)

        # DNS Rows
        self._add_dns_rows(grid, net_data.dns)

        # VPN
        vpn_status = (
            "[bold black on green] ACTIVE [/]"
            if net_data.vpn.active
            else "[text.muted]Inactive[/]"
        )
        grid.add_row("VPN", vpn_status)

        # Telephony & Signal
        telephony = net_data.telephony
        cell_info = "Access Denied" if telephony.carrier == "Access Denied" else "Active"
        sig_strength = telephony.signal_dbm

        grid.add_row("CELL INFO", cell_info)
        grid.add_row("SIGNAL", sig_strength)

        return grid

    def _add_dns_rows(self, grid: Table, dns_data: DNSModel) -> None:
        dns_list = ", ".join(dns_data.servers) if dns_data.servers else "None"
        raw_status = dns_data.status

        dns_status: Text | str
        if raw_status == "OK":
            dns_status = "[status.success]OK[/]"
        else:
            # Cleanly truncate long error strings so they don't break borders
            dns_status = Text(f"FAILED: {raw_status}", style="bold red", overflow="ellipsis")

        grid.add_row("DNS", dns_list)
        grid.add_row("DNS STATUS", dns_status)

    def get_activity_glyph(self, activity: str) -> str:
        mapping = {"inout": "▲▼", "in": "▲", "out": "▼", "idle": "◯"}
        return mapping.get(activity.lower(), "◯")

    def _build_health_grid(self, hardware: HardwareTelemetry) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Storage Capsule Bar
        used = hardware.used_storage_gb
        total = hardware.total_storage_gb
        bar = self.progress.render_capsule_bar(used, total)
        grid.add_row("STORAGE", f"{used:.1f} GB {bar}")

        # Battery & Temp
        battery = hardware.battery

        status = battery.status
        if status in ["DISCONNECTED", "NOT DETECTED"]:
            grid.add_row("BATTERY", "[text.muted]Not Detected[/]")
            grid.add_row("TEMP", "[text.muted]N/A[/]")
            grid.add_row("POWER", "[text.muted]N/A[/]")
            return grid

        is_healthy = status in ["CHARGING", "FULL"]
        badge = self.status_badge.render(status, is_healthy)

        capacity = battery.capacity
        grid.add_row("BATTERY", f"{capacity}  {badge}")
        grid.add_row("TEMP", f"{battery.temp_num:.1f}°C  {self.heatmap.render(battery.temp_num)}")

        # Power Vector
        wattage = battery.wattage
        grid.add_row("POWER", self.power.render(wattage))

        return grid

    def render_network_metrics(self, data: NetworkTelemetry) -> None:
        """Renders the detailed Network Diagnostics view with fixed Termux keys."""
        grid = self.grid_builder.create_base_grid(label_width=14)

        self._render_wifi_panel(grid, data.wifi) 
        self._render_sms_panel(grid, data.sms)
        self._render_connectivity_panel(grid, data)
        self._render_telephony_panel(grid, data.telephony)
        self._render_privileged_metrics(grid, data.telephony.deviceinfo)

        self.console.print(
            Panel(
                grid,
                title="[hud.label] NETWORK DIAGNOSTICS [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def _render_wifi_panel(self, grid: Table, wifi: WifiModel) -> None:
        grid.add_row("[hud.label][b]-- Wi-Fi --[/][/]", "")
        grid.add_row("STATUS", wifi.status)

        if wifi.status == "CONNECTED":
            grid.add_row("SSID", wifi.ssid.upper())
            grid.add_row("IP Address", wifi.ip.upper())
            grid.add_row("RSSI (dBm)", wifi.rssi.upper())
            grid.add_row("Speed (Mbps)", wifi.link_speed.upper())

    def _render_sms_panel(self, grid: Table, sms: SmsModel) -> None:
        grid.add_row("[hud.label][b]-- SMS Analytics --[/][/]", "")
        if sms.total_messages == 0 and not sms.risky_domains:
             grid.add_row("STATUS", "[text.muted]No Messages[/]")
        else:
            grid.add_row("TOTAL MSG", str(sms.total_messages))
            grid.add_row("S/R RATIO", str(sms.sent_recv_ratio))
            grid.add_row("DIVERSITY", str(sms.sender_diversity))
            grid.add_row("PEAK HOUR", f"{sms.peak_hour}:00")
            grid.add_row("DOMAINS", str(sms.domain_count))

            if sms.risky_domains:
                grid.add_row("RISK", f"[status.error]{sms.risky_domains[0]}[/]")

    def _render_connectivity_panel(self, grid: Table, data: NetworkTelemetry) -> None:
        hs_status: str = (
            "[status.warning]ACTIVE[/]"
            if data.hotspot_active
            else "[text.muted]Inactive[/]"
        )

        vpn_status: str = (
            f"[status.success]Active ({data.vpn.ip})[/]"
            if data.vpn.active
            else "[text.muted]Inactive[/]"
        )

        grid.add_row("", "")
        grid.add_row("[hud.label][b]-- Connectivity --[/][/]", "")

        grid.add_row("FABRIC", data.fabric)
        grid.add_row("HOTSPOT", hs_status)
        grid.add_row("VPN", vpn_status)

    def _render_telephony_panel(self, grid: Table, telephony: TelephonyModel) -> None:
        device = telephony.deviceinfo
        
        grid.add_row("Carrier", telephony.carrier.upper())
        grid.add_row("Network Type", telephony.cell_type.upper())
        grid.add_row("Data State", device.data_state.upper())
        grid.add_row("Data Enabled", "Yes" if device.data_enabled else "No")
        grid.add_row("Data Activity", device.data_activity.upper())
        grid.add_row("Roaming", "Yes" if device.roaming else "No")
        grid.add_row("Phone Type", device.phone_type.upper())
        grid.add_row("SIM State", device.sim_state.upper())

    def _render_privileged_metrics(self, grid: Table, device: DeviceModel) -> None:
        grid.add_row("", "")
        grid.add_row("[hud.label][b]-- Privileged (Requires Root) --[/][/]", "")

        device_id_val = device.device_id if device.device_id != "N/A" else "[text.muted]Not Available[/]"
        grid.add_row("Device Id", device_id_val)
        sim_sub_val = device.sim_subscriber_id if device.sim_subscriber_id != "N/A" else "[text.muted]Not Available[/]"
        grid.add_row("Sim Subscriber Id", sim_sub_val)
        sim_ser_val = device.sim_serial_number if device.sim_serial_number != "N/A" else "[text.muted]Not Available[/]"
        grid.add_row("Sim Serial Number", sim_ser_val)

    def render_security_metrics(self, security: SecurityAuditModel):
        """Renders the Security Audit panel."""
        grid = self.grid_builder.create_base_grid(label_width=16)

        grid.add_row("ROOT STATE", security.root_state)
        grid.add_row("SELINUX", security.selinux)
        grid.add_row("LD_PRELOAD", security.ld_preload)
        grid.add_row("SUID ANOMALIES", str(security.suid_anomalies))

        self.console.print(
            Panel(
                grid,
                title="[hud.label] SECURITY AUDIT [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def _build_sensor_grid(self, sensor_data: dict[str, object]) -> Table:
        grid = self.grid_builder.create_base_grid(label_width=12)
        grid.add_row("[hud.label][b]-- SENSOR DATA --[/][/]", "")

        if "error" in sensor_data:
            grid.add_row("STATUS", "[status.error]Failed[/]")
        else:
            for sensor, data in sensor_data.items():
                # Aesthetic formatting for sensor values
                if isinstance(data, dict):
                    val = next(iter(data.values()))
                    label = sensor[:10].upper()
                    formatted = f"{val:.2f}" if isinstance(val, (int, float)) else str(val)
                    grid.add_row(label, formatted)
        return grid

    def render_package_manager(self, data: dict[str, object]):
        """Renders installed package listings cleanly."""
        pkgs = cast(list[object], data.get("packages", []))
        table = Table(
            title="\n[text.primary]Installed Packages[/]",
            box=box.MINIMAL,
            border_style="border.main",
            expand=True,
        )
        table.add_column("IDX", style="hud.label", justify="right", width=6)
        table.add_column("Package Name", style="hud.value")

        if not pkgs:
            table.add_row("-", "No packages found.")
        else:
            for i, pkg in enumerate(pkgs[:20], 1):
                table.add_row(str(i), str(pkg))

        self.console.print(table)
        if len(pkgs) > 20:
            self.console.print(
                f"  [text.muted]↳ ... and {len(pkgs) - 20} more packages hidden[/]\n"
            )
