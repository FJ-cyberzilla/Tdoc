"""
UI Views for the Termux-Doctor console interface.
"""

import os

from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from src.constants import __version__

from .grid import GridBuilder
from .visuals import Visualizer


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
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        table.add_column("Key", style="accent.secondary", justify="right")
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

    def render_package_manager(self, data: dict):
        """Renders the package manager output using a minimalist aesthetic table."""
        pkgs = data.get("packages", [])
        table = Table(
            title="\n[text.primary]Installed Packages[/]",
            box=box.MINIMAL,
            border_style="border.main",
        )
        table.add_column("IDX", style="hud.label", justify="right")
        table.add_column("Package Name", style="hud.value")

        if not pkgs:
            table.add_row("-", "No packages found.")
        else:
            for i, pkg in enumerate(pkgs[:20], 1):
                table.add_row(str(i), pkg)

        self.console.print(table)
        if len(pkgs) > 20:
            self.console.print(
                f"  [text.muted]↳ ... and {len(pkgs) - 20} more packages hidden[/]\n"
            )

    def render_dashboard(self, env_data: dict, net_data: dict, health_data: dict):
        """Renders the high-density dashboard grid."""
        layout = Layout()
        layout.split_column(Layout(name="header", size=3), Layout(name="body"))
        layout["body"].split_row(Layout(name="left"), Layout(name="right"))

        env_panel = Panel(
            self._build_env_grid(env_data),
            title="[hud.label] SYSTEM HARDWARE [/]",
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
        )
        health_panel = Panel(
            self._build_health_grid(health_data),
            title="[hud.label] STORAGE & POWER [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )

        layout["header"].update(
            Panel(
                "[text.primary]LIVE TELEMETRY[/] [text.muted]• Cybertronic Systems[/]",
                style="header.main",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )
        layout["left"].split_column(env_panel, health_panel)
        layout["right"].update(net_panel)
        self.console.print(layout)

    def _build_env_grid(self, env_data: dict) -> Table:
        grid = self.grid_builder.create_base_grid()
        grid.add_row(
            "CPU", f"{env_data['cpu']['model']} [hud.unit]({env_data['cpu']['cores']} cores)[/]"
        )
        grid.add_row(
            "RAM",
            f"{env_data['ram']['used']:.1f} GB [text.muted]/[/] {env_data['ram']['total']:.1f} GB",
        )
        grid.add_row("UPTIME", f"{env_data['uptime']}")
        return grid

    def _build_net_grid(self, net_data: dict) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Add basic rows
        activity = net_data.get("activity", "idle")
        grid.add_row("FABRIC", f"{self.get_activity_glyph(activity)} {activity.upper()}")
        grid.add_row("LOCAL IP", f"{net_data['local_ip']}")

        # Add DNS rows
        self._add_dns_rows(grid, net_data["dns"])

        # Add status rows
        vpn_status = (
            "[status.success]Active[/]" if net_data["vpn"]["active"] else "[text.muted]Inactive[/]"
        )
        grid.add_row("VPN", vpn_status)

        # Add telephony rows
        telephony = net_data["telephony"]
        cell_info = "Access Denied" if "error" in telephony.get("cellinfo", {}) else "Active"
        sig_strength = self._format_signal_strength(telephony)
        grid.add_row("CELL INFO", cell_info)
        grid.add_row("SIGNAL", sig_strength)

        return grid

    def _add_dns_rows(self, grid: Table, dns_data: dict):
        dns_list = ", ".join(dns_data["servers"]) if dns_data["servers"] else "None"
        dns_status = (
            dns_data["status"]
            if dns_data["status"] == "OK"
            else f"[status.critical]{dns_data['status']}[/]"
        )
        grid.add_row("DNS", dns_list)
        grid.add_row("DNS STATUS", dns_status)

    def _format_signal_strength(self, telephony: dict) -> str:
        if "error" not in telephony.get("signalstrength", {}):
            return str(telephony["signalstrength"].get("dbm", "N/A")) + " dBm"
        return "N/A"

    def get_activity_glyph(self, activity: str) -> str:
        """Maps activity to visual glyphs."""
        mapping = {"inout": "▲▼", "in": "▲", "out": "▼", "idle": "◯"}
        return mapping.get(activity.lower(), "◯")

    def _build_health_grid(self, health_data: dict) -> Table:
        grid = self.grid_builder.create_base_grid()

        # Capsule bar for storage
        used = health_data.get("used_storage_gb", 0)
        total = health_data.get("total_storage_gb", 100)
        bar = self.render_capsule_bar(used, total)
        grid.add_row("STORAGE", f"{used:.1f} GB {bar}")

        battery = health_data.get("battery", {})
        temp = battery.get("temp_num", 0)  # Use numeric

        # Heatmap for temperature
        temp_viz = self.visualizer.render_gradient_heatmap(temp)

        # State Badge
        status = battery.get("status", "UNKNOWN")
        if status == "DISCONNECTED":
            grid.add_row("BATTERY", "[text.muted]Not Detected[/]")
            grid.add_row("TEMP", "[text.muted]N/A[/]")
            grid.add_row("POWER", "[text.muted]N/A[/]")
            return grid

        is_healthy = status in ["CHARGING", "FULL"]
        badge = self.visualizer.render_state_badge(status, is_healthy)

        grid.add_row("BATTERY", f"{battery.get('capacity', 'N/A')} {badge}")
        grid.add_row("TEMP", f"{temp}°C {temp_viz}")

        # Power Vector
        wattage = battery.get("wattage", 0.0)
        grid.add_row("POWER", self.visualizer.render_power_vector(wattage))

        return grid

    def render_capsule_bar(self, used: float, total: float) -> str:
        """Helper to render a capsule bar."""
        # Simple implementation for now, should probably move to visuals.py later
        percent = (used / total) * 10 if total > 0 else 0
        return f"[{'█' * int(percent)}{'░' * (10 - int(percent))}]"

    def render_network_metrics(self, data: dict):
        grid = self.grid_builder.create_base_grid()
        self._add_vpn_and_hotspot_rows(grid, data)
        self._add_telephony_rows(grid, data)
        self.console.print(
            Panel(
                grid,
                title="[hud.label] NETWORK DIAGNOSTICS [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def _add_vpn_and_hotspot_rows(self, grid: Table, data: dict):
        hs_status = (
            "[status.warning]Active[/]" if data["hotspot_active"] else "[status.success]Inactive[/]"
        )
        vpn_status = (
            f"[status.success]Active ({data['vpn']['ip']})[/]"
            if data["vpn"]["active"]
            else "[text.muted]Inactive[/]"
        )
        grid.add_row("FABRIC", f"{data['topology']['fabric']}")
        grid.add_row("HOTSPOT", hs_status)
        grid.add_row("VPN", vpn_status)

    def _add_telephony_rows(self, grid: Table, data: dict):
        telephony = data["telephony"]
        device = telephony.get("deviceinfo", {})
        cell = telephony.get("cellinfo", {})

        carrier = (
            device.get("carrier_name", "N/A")
            if "error" not in device
            else "[status.critical]Access Denied[/]"
        )
        cell_type = (
            cell[0].get("type", "N/A") if isinstance(cell, list) and len(cell) > 0 else "N/A"
        )

        grid.add_row("CARRIER", carrier)
        grid.add_row("CELL TYPE", cell_type)

    def render_security_metrics(self, data: dict):
        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="hud.label", justify="right", width=16)
        grid.add_column(style="hud.value")
        grid.add_row("ROOT STATE", data["root_presence"]["message"])
        grid.add_row("SELINUX", data["selinux"])
        grid.add_row("LD_PRELOAD", data["ld_preload"]["message"])
        grid.add_row("SUID ANOMALIES", str(data["termux_suid"]))
        self.console.print(
            Panel(
                grid,
                title="[hud.label] SECURITY AUDIT [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def render_updater_metrics(self, data: dict):
        grid = self.grid_builder.create_base_grid()
        sync_state = (
            "[status.success]Synced[/]" if data["synced"] else "[status.critical]Desynced[/]"
        )
        grid.add_row("GIT STATUS", data["git_status"])
        grid.add_row("SYNC STATE", sync_state)
        self.console.print(
            Panel(
                grid,
                title="[hud.label] WORKSPACE STATUS [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )
