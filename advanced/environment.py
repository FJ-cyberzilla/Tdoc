"""
TDoc Environment Subsystem - System Profiler & Termux Ecosystem Analysis
"""

import os
import platform
import shutil
import subprocess


def get_prop(key: str) -> str:
    """Natively resolves an Android system property value."""
    try:
        res = subprocess.run(
            ["getprop", key], capture_output=True, text=True, check=False
        )
        return res.stdout.strip() if res.returncode == 0 else ""
    except Exception:
        return ""


def run_environment_checks() -> dict:
    """Evaluates cross-platform environmental properties and ecosystem status."""
    print("\n🖥 --- [ MACHINE IDENTITY & SYSTEM PLATFORM ] ---")

    # 1. Cross-Platform Hardware & OS Profiler
    is_android = bool(shutil.which("getprop"))

    if is_android:
        manufacturer = get_prop("ro.product.manufacturer").upper() or "ANDROID"
        model = get_prop("ro.product.model") or "DEVICE"
        version = get_prop("ro.build.version.release")
        sdk = get_prop("ro.build.version.sdk")
        build_id = get_prop("ro.build.id")

        print(f"  ✓ Device Identity         : {manufacturer} {model}")
        print(f"  ✓ Android Runtime Version : OS {version} (API Level {sdk})")
        print(f"  ✓ System Compile Build ID : {build_id}")
    else:
        sys_type = platform.system()
        release = platform.release()
        arch = platform.machine()
        print(f"  ✓ Device Identity         : Generic {sys_type} Host")
        print(f"  ✓ OS Kernel Release       : {release} ({arch})")
        print(f"  ✓ System Compile Build ID : STABLE_PC_INSTANCE")

    # 2. Termux-Specific Environment Verification
    print("  ✓ Terminal Encoding Node  : " + os.environ.get("LANG", "en_US.UTF-8"))

    api_connected = (
        "CONNECTED" if shutil.which("termux-battery-status") else "UNAVAILABLE"
    )
    print(f"  ▪ Termux:API Ecosystem    : {api_connected}")

    boot_dir = "/data/data/com.termux/files/home/.termux/boot"
    boot_status = (
        "ACTIVE" if os.path.exists(boot_dir) else "INACTIVE (No startup hooks)"
    )
    print(f"  ▪ Termux:Boot Nodes       : {boot_status}")

    return {
        "is_android": is_android,
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
    }
