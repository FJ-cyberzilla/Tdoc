"""
TDoc Core Management Interface - Hardened HUD Router with Custom System Branding
"""

import os
from typing import Any

from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from src.constants import __version__
from src.core.theme import ThemeManager
from src.router import TDocRouter


class UIRenderer:
    """Handles rendering of high-density, modern terminal UI components."""

    def __init__(self, theme_manager: ThemeManager):
        self.theme = theme_manager
        self.console = theme_manager.console

    def clear_screen(self):
        """Wipes terminal view buffer."""
        os.system("clear" if os.name != "nt" else "cls")

    def render_header(self):
        """Renders the sleek top branding banner."""
        # A minimal, modern header bypassing heavy ASCII art
        header = Table.grid(padding=(0, 1), expand=True)
        header.add_column(justify="left", ratio=1)
        header.add_column(justify="right")

        header.add_row(
            "[accent.primary]⚡ T-DOC[/] [text.muted]::[/] [text.primary]FJ™ Cybertronic[/]",
            f"[text.muted]v{__version__}[/]",
        )

        self.console.print(
            Panel(
                header,
                box=box.ROUNDED,
                border_style="border.main",
                padding=(0, 2),
            )
        )

    def render_navigation(self):
        """Renders the TDoc main menu navigation as a clean, aligned grid."""
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        table.add_column("Key", style="accent.secondary", justify="right")
        table.add_column("Action", style="text.primary")
        table.add_column("Module", style="text.muted")

        table.add_row("1", "Telemetry Dashboard", "• Hardware, HDD, Env")
        table.add_row("2", "Network Deep-Dive", "• DNS Leak, Latency, Hotspot")
        table.add_row("3", "Security Audit", "• SUID, Root, SELinux")
        table.add_row("4", "Workspace Status", "• Git Status, Sync")
        table.add_row("5", "Package Manager", "• Installed Packages")
        table.add_row("6", "Run Htop", "• Process Monitor")
        table.add_row("7", "Run Neofetch", "• System Info")
        table.add_row("0", "Exit System", "")

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

        # box.MINIMAL gives top and bottom lines without vertical dividers
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
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
        )
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

        # 1. Environment Panel
        env_panel = Panel(
            self._build_env_grid(env_data),
            title="[hud.label] SYSTEM HARDWARE [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )
        # 2. Network Panel
        net_panel = Panel(
            self._build_net_grid(net_data),
            title="[hud.label] NETWORK FABRIC [/]",
            title_align="left",
            border_style="border.dashboard",
            box=box.ROUNDED,
        )
        # 3. Health/Storage Panel
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

    # -------------------------------------------------------------------------
    # Private Grid Builders (Replaces messy Text append logic with perfect columns)
    # -------------------------------------------------------------------------

    def _create_base_grid(self) -> Table:
        """Helper to generate perfectly aligned key-value invisible tables."""
        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="hud.label", justify="right", width=12)
        grid.add_column(style="hud.value")
        return grid

    def _build_env_grid(self, env_data: dict) -> Table:
        grid = self._create_base_grid()
        grid.add_row(
            "CPU",
            f"{env_data['cpu']['model']} [hud.unit]({env_data['cpu']['cores']} cores)[/]",
        )
        grid.add_row(
            "RAM",
            f"{env_data['ram']['used']:.1f} GB [text.muted]/[/] {env_data['ram']['total']:.1f} GB",
        )
        grid.add_row("UPTIME", f"{env_data['uptime']}")
        return grid

    def _build_net_grid(self, net_data: dict) -> Table:
        grid = self._create_base_grid()

        vpn_status = (
            "[status.success]Active[/]" if net_data["vpn"]["active"] else "[text.muted]Inactive[/]"
        )
        dns_data = net_data["dns"]
        dns_list = ", ".join(dns_data["servers"]) if dns_data["servers"] else "None"
        dns_status = (
            dns_data["status"]
            if dns_data["status"] == "OK"
            else f"[status.critical]{dns_data['status']}[/]"
        )

        grid.add_row("LOCAL IP", f"{net_data['local_ip']}")
        grid.add_row("DNS", dns_list)
        grid.add_row("DNS STATUS", dns_status)
        grid.add_row("VPN", vpn_status)
        grid.add_row("ISP", f"{net_data['vpn']['isp']}")
        return grid

    def _build_health_grid(self, health_data: dict) -> Table:
        grid = self._create_base_grid()
        grid.add_row("STORAGE", f"{health_data.get('used_storage_gb', 0):.1f} [hud.unit]GB[/]")
        battery = health_data.get("battery", {})
        grid.add_row(
            "BATTERY",
            f"{battery.get('capacity', 'N/A')} [hud.unit]({battery.get('status', 'N/A')})[/]",
        )
        grid.add_row("TEMP", f"{battery.get('temp', 'N/A')}")
        return grid

    def render_network_metrics(self, data: dict):
        """Renders standalone network diagnostics."""
        grid = self._create_base_grid()

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

        self.console.print(
            Panel(
                grid,
                title="[hud.label] NETWORK DIAGNOSTICS [/]",
                title_align="left",
                box=box.ROUNDED,
                border_style="border.main",
            )
        )

    def render_security_metrics(self, data: dict):
        """Renders security audit findings."""
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
        """Renders workspace status."""
        grid = self._create_base_grid()

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


class HUDLoop:
    """Manages the UI interaction loop."""

    def __init__(self, router: TDocRouter, utility_service: Any):
        self.router = router
        self.utility_service = utility_service
        self.theme = ThemeManager()
        self.renderer = UIRenderer(self.theme)

    def start(self):
        """Runs the UI interaction loop."""
        while True:
            self.renderer.clear_screen()
            self.renderer.render_header()
            self.renderer.render_navigation()

            try:
                # Modern sleek prompt utilizing the raw ANSI properties from ThemeManager
                prompt = f"\n{self.theme.cyan}▲{self.theme.reset} {self.theme.muted}tdoc ⨠{self.theme.reset} "
                choice = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                self.theme.console.print("\n[text.muted]Session terminated by user.[/]")
                break

            if choice == "0":
                self.theme.console.print("\n[status.success]Diagnostic pipeline closed safely.[/]")
                break

            self._handle_choice(choice)

            # Sleek return prompt
            input(f"\n{self.theme.muted}↵ Press Enter to return...{self.theme.reset}")

    def _handle_choice(self, choice: str):
        """Dispatches choices to appropriate handlers."""
        action_map = {
            "1": ("dashboard", self._handle_dashboard),
            "2": ("network", self._handle_network),
            "3": ("security", self._handle_security),
            "4": ("updater", self._handle_updater),
            "5": ("package_manager", self._handle_package_manager),
            "6": ("htop", lambda _: self.utility_service.run_tool("htop")),
            "7": ("neofetch", lambda _: self.utility_service.run_tool("neofetch")),
        }

        if choice not in action_map:
            self.theme.console.print("\n[error.text] ✘ Invalid operation token [/]")
            return

        action_name, handler = action_map[choice]
        try:
            if action_name in ["htop", "neofetch"]:
                handler(None)
            else:
                result = self.router.route_action(action_name)
                handler(result)
        except Exception as e:
            self.theme.console.print(f"\n[error.text] ✘ Exception: {e} [/]")

    def _handle_dashboard(self, result):
        self.renderer.render_dashboard(
            result["platform"]["environment"], result["network"], result["health"]
        )

    def _handle_network(self, result):
        self.renderer.render_network_metrics(result)

    def _handle_security(self, result):
        self.renderer.render_security_metrics(result)

    def _handle_updater(self, result):
        self.renderer.render_updater_metrics(result)

    def _handle_package_manager(self, result):
        self.renderer.render_package_manager(result)


def start_hud(router: TDocRouter, utility_service: Any):
    """Wrapper function to maintain backward compatibility."""
    loop = HUDLoop(router, utility_service)
    loop.start()
