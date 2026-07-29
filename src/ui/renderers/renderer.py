"""
UI Views and dashboard layout renderers for Termux-Doctor console interface.
"""

import os
from typing import Any

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.constants import __version__

from .visuals import GridBuilder, Visualizer


class UIRenderer:
    """Handles rendering of high-density, modern terminal UI components."""

    def __init__(self, console):
        self.console = console
        self.grid_builder = GridBuilder()
        self.visualizer = Visualizer()

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
        self, env_data: dict[str, Any], net_data: dict[str, Any], health_data: dict[str, Any]
    ) -> Panel:
        """Constructs and returns the dashboard panel for live updates."""

        # Build cards
        env_panel = Panel(
            self._build_env_grid(env_data),
            title="[hud.label] SYSTEM HARDWARE [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

        health_panel = Panel(
            self._build_health_grid(health_data),
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

        sensor_panel = Panel(
            self._build_sensor_grid(env_data.get("sensors", {})),
            title="[hud.label] SENSOR ARRAY [/]",
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
        right_stack.add_row(sensor_panel)

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

    def _build_env_grid(self, env_data: dict[str, Any]) -> Table:
        grid = self.grid_builder.create_base_grid()
        cpu = env_data.get("cpu", {})
        ram = env_data.get("ram", {})

        grid.add_row(
            "CPU", f"{cpu.get('model', 'Android')} [text.muted]({cpu.get('cores', '?')} cores)[/]"
        )
        grid.add_row(
            "RAM",
            f"{ram.get('used', 0.0):.1f} GB [text.muted]/[/] {ram.get('total', 0.0):.1f} GB",
        )
        grid.add_row("UPTIME", f"{env_data.get('uptime', 'N/A')}")
        return grid

    def _build_net_grid(self, net_data: dict[str, Any]) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Network Activity
        activity = net_data.get("activity", "idle")
        glyph = self.get_activity_glyph(activity)
        grid.add_row("FABRIC", f"{glyph} {activity.upper()}")
        grid.add_row("LOCAL IP", f"{net_data.get('local_ip', '127.0.0.1')}")

        # DNS Rows
        self._add_dns_rows(grid, net_data.get("dns", {}))

        # VPN
        vpn_info = net_data.get("vpn", {})
        vpn_status = (
            "[bold black on green] ACTIVE [/]"
            if vpn_info.get("active")
            else "[text.muted]Inactive[/]"
        )
        grid.add_row("VPN", vpn_status)

        # Telephony & Signal
        telephony = net_data.get("telephony", {})
        cell_info = "Access Denied" if "error" in telephony.get("cellinfo", {}) else "Active"
        sig_strength = self._format_signal_strength(telephony)

        grid.add_row("CELL INFO", cell_info)
        grid.add_row("SIGNAL", sig_strength)

        return grid

    def _add_dns_rows(self, grid: Table, dns_data: dict[str, Any]) -> None:
        servers = dns_data.get("servers", [])
        dns_list = ", ".join(servers) if servers else "None"
        raw_status = dns_data.get("status", "OK")

        dns_status: Text | str
        if raw_status == "OK":
            dns_status = "[status.success]OK[/]"
        else:
            # Cleanly truncate long error strings so they don't break borders
            dns_status = Text(f"FAILED: {raw_status}", style="bold red", overflow="ellipsis")

        grid.add_row("DNS", dns_list)
        grid.add_row("DNS STATUS", dns_status)

    def _format_signal_strength(self, telephony: dict[str, Any]) -> str:
        cellinfo = telephony.get("cellinfo", {})
        signalstrength = telephony.get("signalstrength", {})

        if "error" not in signalstrength and "dbm" in signalstrength:
            return f"{signalstrength['dbm']} dBm"
        elif isinstance(cellinfo, list) and len(cellinfo) > 0:
            dbm = cellinfo[0].get("dbm") or cellinfo[0].get("lte_rsrp")
            if dbm:
                return f"{dbm} dBm"
        return "N/A"

    def get_activity_glyph(self, activity: str) -> str:
        mapping = {"inout": "▲▼", "in": "▲", "out": "▼", "idle": "◯"}
        return mapping.get(str(activity).lower(), "◯")

    def _build_health_grid(self, health_data: dict[str, Any]) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Storage Capsule Bar
        used = health_data.get("used_storage_gb", 0.0)
        total = health_data.get("total_storage_gb", 100.0)
        bar = self.visualizer.render_capsule_bar(used, total)
        grid.add_row("STORAGE", f"{used:.1f} GB {bar}")

        # Battery & Temp
        battery = health_data.get("battery", {})
        temp = float(battery.get("temp_num", battery.get("temperature", 0.0)))

        status = str(battery.get("status", "UNKNOWN")).upper()
        if status in ["DISCONNECTED", "NOT DETECTED"]:
            grid.add_row("BATTERY", "[text.muted]Not Detected[/]")
            grid.add_row("TEMP", "[text.muted]N/A[/]")
            grid.add_row("POWER", "[text.muted]N/A[/]")
            return grid

        is_healthy = status in ["CHARGING", "FULL"]
        badge = self.visualizer.render_state_badge(status, is_healthy)

        capacity = battery.get("capacity", battery.get("percentage", "N/A"))
        if isinstance(capacity, (int, float)):
            capacity = f"{capacity}%"

        grid.add_row("BATTERY", f"{capacity}  {badge}")
        grid.add_row("TEMP", f"{temp:.1f}°C  {self.visualizer.render_gradient_heatmap(temp)}")

        # Power Vector
        wattage = float(battery.get("wattage", 0.0))
        grid.add_row("POWER", self.visualizer.render_power_vector(wattage))

        return grid

    def render_network_metrics(self, data: dict[str, Any]) -> None:
        """Renders the detailed Network Diagnostics view with fixed Termux keys."""
        grid = self.grid_builder.create_base_grid(label_width=14)

        self._render_wifi_panel(grid, data.get("wifi", {}))
        self._render_sms_panel(grid, data.get("sms", {}))
        self._render_connectivity_panel(grid, data)
        self._render_telephony_panel(grid, data.get("telephony", {}))
        self._render_privileged_metrics(grid, data.get("telephony", {}).get("deviceinfo", {}))

        self.console.print(
            Panel(
                grid,
                title="[hud.label] NETWORK DIAGNOSTICS [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def _render_wifi_panel(self, grid: Table, wifi_info: dict[str, Any]) -> None:
        wifi_status: str = str(wifi_info.get("status", "ERROR"))
        grid.add_row("[hud.label][b]-- Wi-Fi --[/][/]", "")
        grid.add_row("STATUS", wifi_status)

        if wifi_status == "CONNECTED":
            wifi_map = {
                "ssid": "SSID",
                "ip": "IP Address",
                "rssi": "RSSI (dBm)",
                "link_speed_mbps": "Speed (Mbps)",
            }
            for key, label in wifi_map.items():
                grid.add_row(label, str(wifi_info.get(key, "N/A")).upper())

    def _render_sms_panel(self, grid: Table, sms_info: dict[str, Any]) -> None:
        grid.add_row("[hud.label][b]-- SMS Analytics --[/][/]", "")
        if "error" in sms_info:
            grid.add_row("STATUS", "[status.error]Analysis Failed[/]")
        else:
            grid.add_row("TOTAL MSG", str(sms_info.get("total_messages")))
            grid.add_row("S/R RATIO", str(sms_info.get("sent_recv_ratio")))
            grid.add_row("DIVERSITY", str(sms_info.get("sender_diversity")))
            grid.add_row("PEAK HOUR", f"{sms_info.get('peak_hour')}:00")
            grid.add_row("DOMAINS", str(sms_info.get("domain_count")))

            risky: list[str] = sms_info.get("risky_domains", [])
            if risky:
                grid.add_row("RISK", f"[status.error]{risky[0]}[/]")

    def _render_connectivity_panel(self, grid: Table, data: dict[str, Any]) -> None:
        hotspot_info: dict[str, Any] = data.get("hotspot", {"active": False, "type": "None"})
        hs_status: str = (
            f"[status.warning]{hotspot_info['type']}[/]"
            if hotspot_info.get("active")
            else "[text.muted]Inactive[/]"
        )

        vpn_info: dict[str, Any] = data.get("vpn", {})
        vpn_ip: str = str(vpn_info.get("ip", "N/A"))
        vpn_status: str = (
            f"[status.success]Active ({vpn_ip})[/]"
            if vpn_info.get("active")
            else "[text.muted]Inactive[/]"
        )

        grid.add_row("", "")
        grid.add_row("[hud.label][b]-- Connectivity --[/][/]", "")

        topology: dict[str, Any] = data.get("topology", {})
        grid.add_row("FABRIC", f"{topology.get('fabric', 'CELLULAR')}")
        grid.add_row("HOTSPOT", hs_status)
        grid.add_row("VPN", vpn_status)

    def _render_telephony_panel(self, grid: Table, telephony: dict[str, Any]) -> None:
        device: dict[str, Any] = telephony.get("deviceinfo", {})

        key_map = {
            "network_operator_name": "Carrier",
            "network_type": "Network Type",
            "data_state": "Data State",
            "data_enabled": "Data Enabled",
            "data_activity": "Data Activity",
            "network_roaming": "Roaming",
            "phone_type": "Phone Type",
            "sim_state": "SIM State",
        }

        for key, label in key_map.items():
            value: Any = device.get(key)
            if value is not None:
                if isinstance(value, bool):
                    formatted_value: str = "Yes" if value else "No"
                elif value == "true":
                    formatted_value = "Yes"
                elif value == "false":
                    formatted_value = "No"
                else:
                    formatted_value = str(value)

                grid.add_row(label, formatted_value.upper())

    def _render_privileged_metrics(self, grid: Table, device: dict[str, Any]) -> None:
        grid.add_row("", "")
        grid.add_row("[hud.label][b]-- Privileged (Requires Root) --[/][/]", "")

        privileged_keys: list[str] = [
            "device_id",
            "sim_subscriber_id",
            "sim_serial_number",
        ]

        for key in privileged_keys:
            value: Any = device.get(key)
            label: str = key.replace("_", " ").title()
            grid.add_row(label, str(value) if value else "[text.muted]Not Available[/]")


    def render_security_metrics(self, data: dict[str, Any]):
        """Renders the Security Audit panel."""
        grid = self.grid_builder.create_base_grid(label_width=16)

        root_info = data.get("root_presence", {})
        root_msg = (
            root_info.get("message", "Unknown") if isinstance(root_info, dict) else str(root_info)
        )

        ld_info = data.get("ld_preload", {})
        ld_msg = ld_info.get("message", "Clean") if isinstance(ld_info, dict) else str(ld_info)

        grid.add_row("ROOT STATE", root_msg)
        grid.add_row("SELINUX", str(data.get("selinux", "Enforcing")))
        grid.add_row("LD_PRELOAD", ld_msg)
        grid.add_row("SUID ANOMALIES", str(data.get("termux_suid", 0)))

        self.console.print(
            Panel(
                grid,
                title="[hud.label] SECURITY AUDIT [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def _build_sensor_grid(self, sensor_data: dict[str, Any]) -> Table:
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

    def render_package_manager(self, data: dict[str, Any]):
        """Renders installed package listings cleanly."""
        pkgs = data.get("packages", [])
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
