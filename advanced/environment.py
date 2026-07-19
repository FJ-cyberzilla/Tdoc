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
    is_android = bool(shutil.which("getprop"))

    results = {
        "is_android": is_android,
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
    }

    if is_android:
        results["manufacturer"] = get_prop("ro.product.manufacturer").upper() or "ANDROID"
        results["model"] = get_prop("ro.product.model") or "DEVICE"
        results["version"] = get_prop("ro.build.version.release")
        results["sdk"] = get_prop("ro.build.version.sdk")
        results["build_id"] = get_prop("ro.build.id")
    else:
        results["manufacturer"] = "Generic"
        results["model"] = platform.system()
        results["version"] = platform.release()
        results["sdk"] = "N/A"
        results["build_id"] = "STABLE_PC_INSTANCE"

    results["lang"] = os.environ.get("LANG", "en_US.UTF-8")
    results["api_connected"] = bool(shutil.which("termux-battery-status"))
    results["boot_status"] = os.path.exists("/data/data/com.termux/files/home/.termux/boot")

    return results
