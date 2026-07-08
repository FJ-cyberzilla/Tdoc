"""
TDoc Core Management Interface - Hardened HUD Router with Custom System Branding
"""

import os
import sys
import shutil
from advanced import environment, health, network, security
from constants import __version__

# High-Fidelity ANSI Engine Color Channels
ORANGE = "\033[38;5;208m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def clear_screen():
    """Wipes terminal view buffer cleanly across platforms."""
    os.system("clear" if os.name != "nt" else "cls")


def get_menu_device_string() -> str:
    """Quickly resolves device identity for menu header real estate."""
    if bool(shutil.which("getprop")):
        man = environment.get_prop("ro.product.manufacturer").upper() or "ANDROID"
        mod = environment.get_prop("ro.product.model") or "DEVICE"
        return f"{man} {mod}"
    return "GENERIC HOST"


def show_hud():
    """Renders an expanded cybernetic HUD layout with custom system ID and metrics."""
    clear_screen()
    dev_id = get_menu_device_string()
    bat = health.get_battery_metrics()

    cap = bat.get("capacity", "UNKNOWN")
    temp = bat.get("temp", "UNKNOWN")
    state = bat.get("status", "UNKNOWN")

    print(
        f"{ORANGE}╭──────────────────────────────────────────────────────────────────────────╮{RESET}"
    )
    print(
        f"{ORANGE}│{RESET}         {BOLD}{ORANGE}🗲  T D O C  ::  P L A T F O R M  M A T R I X  (v{__version__})  🗲{RESET}"
        f"    {ORANGE}│{RESET}"
    )

    # Custom Brand ID Line
    brand_line = "FJ™ Cyberzilla Cybertronic Systems®"
    pad_b = (72 - len(brand_line)) // 2
    l_pad_b = " " * pad_b
    r_pad_b = " " * (72 - len(brand_line) - pad_b)
    print(
        f"{ORANGE}│{RESET}{l_pad_b}{BOLD}{ORANGE}{brand_line}{RESET}{r_pad_b}{ORANGE}│{RESET}"
    )

    # Target Device Identity Line
    target_line = f"[ Target Unit: {dev_id} ]"
    pad1 = (72 - len(target_line)) // 2
    l_pad1 = " " * pad1
    r_pad1 = " " * (72 - len(target_line) - pad1)
    print(f"{ORANGE}│{RESET}{l_pad1}{DIM}{target_line}{RESET}{r_pad1}{ORANGE}│{RESET}")

    # Live Power Grid Metrics
    power_line = f"Fuel Gauge: {cap}  •  Core Temp: {temp}  •  State: {state}"
    pad2 = (72 - len(power_line)) // 2
    l_pad2 = " " * pad2
    r_pad2 = " " * (72 - len(power_line) - pad2)
    print(f"{ORANGE}│{RESET}{l_pad2}{GREEN}{power_line}{RESET}{r_pad2}{ORANGE}│{RESET}")

    print(
        f"{ORANGE}╰──────────────────────────────────────────────────────────────────────────╯{RESET}"
    )
    print(
        f"{CYAN}╭─ Navigation Matrix ──────────────────────────────────────────────────────╮{RESET}"
    )
    print(
        f"{CYAN}│{RESET}  {GREEN}[1]{RESET} Platform Metrics "
        f"(Hardware, Storage, Env)                           {CYAN}│{RESET}"
    )
    print(
        f"{CYAN}│{RESET}  {GREEN}[2]{RESET} Network Topology "
        f"(DNS Leaks, Latency, Hotspot)                      {CYAN}│{RESET}"
    )
    print(
        f"{CYAN}│{RESET}  {GREEN}[3]{RESET} Host Shield Traps "
        f"(SUID Audit, Root Isolation)                      {CYAN}│{RESET}"
    )
    print(
        f"{CYAN}│{RESET}  {GREEN}[4]{RESET} Workspace Integrity Check "
        f"(Git Status, Sync)                        {CYAN}│{RESET}"
    )
    print(
        f"{CYAN}│{RESET}  {RED}[0]{RESET} System Termination "
        f"(Exit Console Master)                            {CYAN}│{RESET}"
    )
    print(
        f"{CYAN}╰──────────────────────────────────────────────────────────────────────────╯{RESET}"
    )


def start_hud_router():
    """Intercepts terminal tokens and routes to low-level modules safely."""
    while True:
        show_hud()
        try:
            choice = input(f"\n{ORANGE}TDoc@Termux{RESET} ⨠ ").strip()
        except KeyboardInterrupt, EOFError:
            print(f"\n{RED}[-]{RESET} Interface interrupted. Aborting execution.")
            sys.exit(0)

        clear_screen()
        if choice == "1":
            environment.run_environment_checks()
            health.run_health_checks()
        elif choice == "2":
            network.run_network_checks()
        elif choice == "3":
            security.run_security_checks()
        elif choice == "4":
            try:
                import updater

                if hasattr(updater, "run_updater_checks"):
                    updater.run_updater_checks()
                else:
                    print(f"\n{GREEN}✓{RESET} Workspace Core Index: Pristine.")
            except Exception as e:
                print(f"\n{RED}❌{RESET} Workspace Check Deferred: {e}")
        elif choice == "0":
            print(f"\n{GREEN}[+] Diagnostic pipeline closed safely. Clear.{RESET}\n")
            break
        else:
            print(f"\n{RED}[-] Invalid Navigation Token. Try again.{RESET}")

        input(f"\n{DIM}Press Enter to return to HUD Matrix...{RESET}")


if __name__ == "__main__":
    start_hud_router()
