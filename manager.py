"""
TDoc Command Center - UI Terminal Control HUD Loop
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

import constants
import helper
import engine
import updater
from advanced import environment, network, health, security

console = Console(theme=Theme(constants.ORANGE_THEME))


def clear_terminal() -> None:
    """Refreshes the control panel layout without screen tearing."""
    os.system("clear" if os.name != "nt" else "cls")


def generate_banner() -> Panel:
    """Builds the SOTA Orange Spectrum tactical HUD layout."""
    banner = Text()
    banner.append(" 🗲  T D O C  ::  P L A T F O R M  D I A G N O S T I C S  🗲 \n", style="banner")
    banner.append(" [ Production Telemetry HUD - Active Terminal Engine ] ", style="text.muted")

    return Panel(
        banner,
        border_style="panel.border",
        title="[status.warning]HUD_STATUS: LIVE[/status.warning]",
        title_align="right",
    )


def display_menu() -> None:
    """Renders the keypad matrix index rules using the custom theme variables."""
    options = (
        " [bold #FF6D00][1][/bold #FF6D00] System Platform Matrix   (Hardware, Storage, Environment)\n"
        " [bold #FF6D00][2][/bold #FF6D00] Advanced Network Core   (Topology, DNS Leak, Latency)\n"
        " [bold #FF6D00][3][/bold #FF6D00] Privacy & Host Security (SUID, Hijack Traps, Root Check)\n"
        " [bold #FF6D00][4][/bold #FF6D00] Workspace Sync Engine   (Git Health, System Auto-Update)\n"
        " [bold #FF3D00][0][/bold #FF3D00] Shut Down System Diagnostics Terminal Console"
    )
    console.print(Panel(
        options,
        title="[text.primary]Keypad Navigation Access Matrix[/text.primary]",
        title_align="left",
        border_style="#FF9100",
        expand=False
    ))


def launch_interface_loop() -> None:
    """Central processing terminal command loop with execution safety gates."""
    while True:
        clear_terminal()
        console.print(generate_banner())
        console.print("")
        display_menu()
        console.print("")

        try:
            choice = console.input("[text.primary]TDoc@Termux ⨠ [/text.primary]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[status.critical]🗲 System exit signature captured.[/status.critical]")
            sys.exit(0)

        console.print("")

        if choice == "1":
            with helper.track_activity("Analyzing environment hardware layers..."):
                console.print("\n[bold #FF6D00]📈 --- [ HARDWARE & BASE PLATFORM ] ---[/bold #FF6D00]")
                health.get_cpu_and_mem_usage()
                health.run_storage_io_benchmark()
                health.read_thermal_zones()
                environment.verify_storage_setup()
                environment.verify_termux_api_subsystem()
                environment.check_boot_scripts()
                environment.validate_locale_and_encoding()

        elif choice == "2":
            # The engine runs its own local progressive tracking metrics panels
            console.print("\n[bold #FF6D00]📡 --- [ TOPOLOGY & DISCOVERY ] ---[/bold #FF6D00]")
            network.get_wifi_analysis()
            network.run_dns_leak_test()
            network.check_ipv6_readiness()
            network.check_firewall_rules()
            engine.scan_ports_with_progress()
            engine.run_advanced_ping()

        elif choice == "3":
            with helper.track_activity("Evaluating systemic privilege containment..."):
                console.print("\n[bold #FF6D00]🔒 --- [ PRIVACY & INTEGRITY AUDIT ] ---[/bold #FF6D00]")
                security.run_comprehensive_security_audit()

        elif choice == "4":
            with helper.track_activity("Analyzing directory file structures for drag..."):
                git_status = helper.diagnose_git_overhead()

            if git_status["vulnerable"]:
                console.print(Panel(
                    f"[status.critical]⚠️ Overhead Leak Found:[/status.critical] {git_status['reason']}\n"
                    f"[text.primary]Target Overhead File Volume:[/text.primary] {git_status['file_count']} files.\n"
                    f"[status.warning]Remedy Key:[/status.warning] {git_status['remedy']}",
                    border_style="#FF3D00",
                    title="[status.critical]Performance Exception[/status.critical]"
                ))
            else:
                console.print("[status.optimal]✓ Workspace structural index is pristine.[/status.optimal]")

            console.print("")
            update_available, msg = updater.check_for_updates()
            if update_available:
                console.print(f"[status.warning]🗲 Patch Pending: {msg}[/status.warning]")
                confirm = console.input("[text.primary]Apply update patch? (y/N): [/text.primary]").lower()
                if confirm == "y":
                    updater.perform_upgrade()
            else:
                console.print(f"[status.optimal]✓ Upstream Status: {msg}[/status.optimal]")

        elif choice == "0":
            console.print("[status.warning]🗲 Halting all active telemetry matrices. Console disconnected.[/status.warning]")
            break

        else:
            console.print("[status.critical]❌ Invalid keypad execution routing identifier.[/status.critical]")

        console.input("\n[text.muted]Press Enter to route back to Master Terminal Matrix...[/text.muted]")
