"""
TDoc Core Management Interface - Hardened HUD Router with Custom System Branding
"""

import os
import sys
import shutil
from constants import __version__
from router import TDocRouter

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


def show_hud(router: TDocRouter):
    """Renders an expanded cybernetic HUD layout using router data."""
    clear_screen()
    info = router.get_basic_info()
    dev_id = info.get("device", "UNKNOWN")
    bat = info.get("battery", {})

    cap = bat.get("capacity", "UNKNOWN")
    temp = bat.get("temp", "UNKNOWN")
    state = bat.get("status", "UNKNOWN")

    print(f"{ORANGE}╭──────────────────────────────────────────────────────────────────────────╮{RESET}")
    print(f"{ORANGE}│{RESET}         {BOLD}{ORANGE}🗲  T D O C  ::  P L A T F O R M  M A T R I X  (v{__version__})  🗲{RESET}    {ORANGE}│{RESET}")
    print(f"{ORANGE}╰──────────────────────────────────────────────────────────────────────────╯{RESET}")
    print(f"{CYAN}╭─ Navigation Matrix ──────────────────────────────────────────────────────╮{RESET}")
    print(f"{CYAN}│{RESET}  {GREEN}[1]{RESET} Platform Metrics (Hardware, Storage, Env)  {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {GREEN}[2]{RESET} Network Topology (DNS Leaks, Latency, Hotspot) {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {GREEN}[3]{RESET} Host Shield Traps (SUID Audit, Root Isolation) {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {GREEN}[4]{RESET} Workspace Integrity Check (Git Status, Sync)   {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {RED}[0]{RESET} System Termination (Exit Console Master)      {CYAN}│{RESET}")
    print(f"{CYAN}╰──────────────────────────────────────────────────────────────────────────╯{RESET}")


def start_hud(router: TDocRouter):
    """Intercepts terminal tokens and routes to low-level modules safely via the router."""
    while True:
        show_hud(router)
        try:
            choice = input(f"\n{ORANGE}TDoc@Termux{RESET} ⨠ ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[-]{RESET} Interface interrupted. Aborting execution.")
            sys.exit(0)

        clear_screen()
        action_map = {"1": "platform", "2": "network", "3": "security", "4": "updater"}
        
        if choice in action_map:
            try:
                result = router.route_action(action_map[choice])
                print(f"\n{GREEN}Result:{RESET} {result}")
            except Exception as e:
                print(f"\n{RED}Error:{RESET} {e}")
        elif choice == "0":
            print(f"\n{GREEN}[+] Diagnostic pipeline closed safely. Clear.{RESET}\n")
            break
        else:
            print(f"\n{RED}[-] Invalid Navigation Token. Try again.{RESET}")

        input(f"\n{DIM}Press Enter to return to HUD Matrix...{RESET}")
