"""
TDoc Core Management Interface - Hardened HUD Router with Custom System Branding
"""

import os
from typing import Any
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from src.constants import __version__
from src.router import TDocRouter
from src.core.theme import ThemeManager


class UIRenderer:
    """Handles rendering of terminal UI components."""

    def __init__(self, theme_manager: ThemeManager):
        self.theme = theme_manager
        self.console = theme_manager.console

    def clear_screen(self):
        """Wipes terminal view buffer."""
        os.system("clear" if os.name != "nt" else "cls")

    def render_header(self):
        """Renders the top branding banner."""
        header_text = Text()
        header_text.append("⚡ T-DOC PLATFORM MATRIX ", style="header.main")
        header_text.append(f"(v{__version__})", style="text.muted")

        self.console.print(
            Panel(
                header_text,
                border_style="border.main",
                padding=(0, 2),
            )
        )

    def render_navigation(self):
        """Renders the TDoc main menu navigation."""
        nav_text = Text()
        nav_text.append("[1] Platform Metrics (Hardware, Storage, Env)\n", style="text.primary")
        nav_text.append(
            "[2] Network Topology (DNS Leaks, Latency, Hotspot)\n", style="text.primary"
        )
        nav_text.append("[3] Security Audit (SUID, Root, SELinux)\n", style="text.primary")
        nav_text.append("[4] Workspace Status (Git Status, Sync)\n", style="text.primary")
        nav_text.append("[5] Package Manager (Installed Packages)\n", style="text.primary")
        nav_text.append("[6] Run Htop\n", style="text.primary")
        nav_text.append("[7] Run Neofetch\n", style="text.primary")
        nav_text.append("[0] Exit System", style="text.primary")

        self.console.print(
            Panel(
                nav_text,
                title="[text.primary]Navigation Matrix[/]",
                border_style="border.main",
            )
        )

    def render_package_manager(self, data: dict):
        """Renders the package manager output using an aesthetic table."""
        pkgs = data.get("packages", [])
        
        table = Table(title="Installed Packages", border_style="border.main")
        table.add_column("Index", style="text.muted", justify="right")
        table.add_column("Package Name", style="white")

        if not pkgs:
            table.add_row("-", "No packages found.")
        else:
            # Displaying first 20 as an aesthetic limit
            for i, pkg in enumerate(pkgs[:20], 1):
                table.add_row(str(i), pkg)

        self.console.print(table)
        if len(pkgs) > 20:
            self.console.print(f"[text.muted]... and {len(pkgs) - 20} more[/text.muted]")

    def render_platform_metrics(self, env_data: dict, health_data: dict):
        """Renders platform metrics using a clean, modern panel/table layout."""
        # Environment Panel
        env_table = Text()
        for k, v in env_data.items():
            env_table.append(f"{k.replace('_', ' ').title()}: ", style="text.primary")
            env_table.append(f"{v}\n", style="white")

        # Health Panel
        health_table = Text()
        batt = health_data.get("battery", {})
        health_table.append("Free Storage: ", style="text.primary")
        health_table.append(f"{health_data.get('free_storage_gb', 0):.1f} GB\n", style="white")
        health_table.append("Write Speed: ", style="text.primary")
        health_table.append(f"{health_data.get('write_speed_mb_s', 0):.1f} MB/s\n", style="white")
        health_table.append("Battery: ", style="text.primary")
        health_table.append(
            f"{batt.get('capacity')} ({batt.get('status')}) - {batt.get('temp')}\n", style="white"
        )

        self.console.print(
            Panel(
                env_table,
                title="[text.primary]Environment Metrics[/]",
                border_style="border.main",
            )
        )
        self.console.print(
            Panel(
                health_table,
                title="[text.primary]Hardware Health[/]",
                border_style="border.main",
            )
        )

    def render_network_metrics(self, data: dict):
        """Renders network diagnostics."""
        net_text = Text()
        net_text.append(f"Fabric: {data['topology']['fabric']}\n", style="white")
        net_text.append(
            f"Hotspot: {'Active' if data['hotspot_active'] else 'Inactive'}\n", style="white"
        )
        vpn = data["vpn"]
        net_text.append(
            f"VPN: {'Active' if vpn['active'] else 'Inactive'} ({vpn['ip']})\n", style="white"
        )

        self.console.print(
            Panel(
                net_text,
                title="[text.primary]Network Topology[/]",
                border_style="border.main",
            )
        )

    def render_security_metrics(self, data: dict):
        """Renders security audit findings."""
        sec_text = Text()
        sec_text.append(f"Root: {data['root_presence']['message']}\n", style="white")
        sec_text.append(f"SELinux: {data['selinux']}\n", style="white")
        sec_text.append(f"LD_PRELOAD: {data['ld_preload']['message']}\n", style="white")
        sec_text.append(f"SUID Anomalies: {data['termux_suid']}\n", style="white")

        self.console.print(
            Panel(
                sec_text,
                title="[text.primary]Security Audit[/]",
                border_style="border.main",
            )
        )

    def render_updater_metrics(self, data: dict):
        """Renders workspace status."""
        upd_text = Text()
        upd_text.append(f"Git Status: {data['git_status']}\n", style="white")
        upd_text.append(
            f"Sync State: {'Synced' if data['synced'] else 'Desynced'}\n", style="white"
        )

        self.console.print(
            Panel(
                upd_text,
                title="[text.primary]Workspace Status[/]",
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
                choice = input(f"\n{self.theme.orange}TDoc@Termux{self.theme.reset} ⨠ ").strip()
            except (KeyboardInterrupt, EOFError):
                break

            action_map = {
                "1": "platform",
                "2": "network",
                "3": "security",
                "4": "updater",
                "5": "package_manager",
                "6": "htop",
                "7": "neofetch",
            }

            if choice in action_map:
                action = action_map[choice]
                if action in ["htop", "neofetch"]:
                    self.utility_service.run_tool(action)
                else:
                    try:
                        result = self.router.route_action(action)
                        if action == "platform":
                            self.renderer.render_platform_metrics(
                                result["environment"], result["health"]
                            )
                        elif action == "network":
                            self.renderer.render_network_metrics(result)
                        elif action == "security":
                            self.renderer.render_security_metrics(result)
                        elif action == "updater":
                            self.renderer.render_updater_metrics(result)
                        elif action == "package_manager":
                            self.renderer.render_package_manager(result)
                        else:
                            self.theme.console.print(f"\n[green]Result:[/green] {result}")
                    except Exception as e:
                        self.theme.console.print(f"\n[red]Error:[/red] {e}")
            elif choice == "0":
                self.theme.console.print("\n[green]Diagnostic pipeline closed.[/green]")
                break
            else:
                self.theme.console.print("\n[red]Invalid token.[/red]")

            input("\n\033[33mPress Enter to return...\033[0m")


def start_hud(router: TDocRouter, utility_service: Any):
    """Wrapper function to maintain backward compatibility."""
    loop = HUDLoop(router, utility_service)
    loop.start()
