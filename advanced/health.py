"""
TDoc Hardware Subsystem - System Storage Benchmarks & Clean API Battery Telemetry
"""

import json
import os
import shutil
import subprocess
import time


def get_battery_metrics() -> dict:
    """Queries official Termux API layers to extract exact device hardware statistics."""
    metrics = {"capacity": "UNKNOWN", "temp": "UNKNOWN", "status": "UNKNOWN"}

    # Mode 1: Intercept official unrooted Termux API system layer
    if shutil.which("termux-battery-status"):
        try:
            res = subprocess.run(
                ["termux-battery-status"], capture_output=True, text=True, check=False
            )
            if res.returncode == 0:
                data = json.loads(res.stdout)
                metrics["capacity"] = f"{data.get('percentage', 'UNKNOWN')}%"
                metrics["status"] = str(data.get("status", "UNKNOWN")).upper()

                raw_temp = data.get("temperature", None)
                if raw_temp is not None:
                    metrics["temp"] = f"{float(raw_temp):.1f}°C"
                return metrics
        except Exception:
            pass

    # Mode 2: Absolute Fallback to raw legacy kernel paths if accessible
    base_path = "/sys/class/power_supply/battery"
    if os.path.exists(base_path):
        try:
            # ✅ FIX: Explicit encoding + error handling
            with open(os.path.join(base_path, "capacity"), "r", encoding="utf-8") as f:
                metrics["capacity"] = f.read().strip() + "%"
            with open(os.path.join(base_path, "status"), "r", encoding="utf-8") as f:
                metrics["status"] = f.read().strip().upper()
            with open(os.path.join(base_path, "temp"), "r", encoding="utf-8") as f:
                metrics["temp"] = f"{float(f.read().strip()) / 10:.1f}°C"
        except (FileNotFoundError, PermissionError, ValueError, UnicodeDecodeError):
            pass

    return metrics


def run_health_checks() -> dict:
    """Evaluates storage delta speeds and maps live power infrastructure."""
    results = {}
    
    try:
        total, used, free = shutil.disk_usage("/")
        results["memory_overhead"] = (used / total) * 100
        results["free_memory_mb"] = free // (1024 * 1024)
    except Exception:
        results["memory_overhead"] = None
        results["free_memory_mb"] = None

    test_file = "io_perf.tmp"
    data = os.urandom(1024 * 1024 * 25)
    start = time.time()
    try:
        with open(test_file, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        delta = time.time() - start
        results["write_speed_mb_s"] = 25 / delta
        os.remove(test_file)
    except Exception:
        results["write_speed_mb_s"] = None

    bat = get_battery_metrics()
    results["battery"] = bat
    
    return results
