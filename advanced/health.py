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

                # Format temperature conversion safely
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
            with open(os.path.join(base_path, "capacity"), "r") as f:
                metrics["capacity"] = f.read().strip() + "%"
            with open(os.path.join(base_path, "status"), "r") as f:
                metrics["status"] = f.read().strip().upper()
            with open(os.path.join(base_path, "temp"), "r") as f:
                metrics["temp"] = f"{float(f.read().strip()) / 10:.1f}°C"
        except Exception:
            pass

    return metrics


def run_health_checks() -> dict:
    """Evaluates storage delta speeds and maps live power infrastructure."""
    print("\n📈 --- [ HARDWARE & BASE PLATFORM ] ---")

    try:
        total, used, free = shutil.disk_usage("/")
        available_mb = free // (1024 * 1024)
        overhead = (used / total) * 100
        print(
            f"  ✓ Memory Overhead         : {overhead:.1f}% used ({available_mb} MB Available)"
        )
    except Exception:
        print("  ❌ Memory Overhead         : ACCESS BOUNDARY VIOLATION")

    test_file = "io_perf.tmp"
    data = os.urandom(1024 * 1024 * 25)
    start = time.time()
    try:
        with open(test_file, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        delta = time.time() - start
        write_speed = 25 / delta
        print(f"  ✓ Internal Flash Storage  : {write_speed:.2f} MB/s Write Delta")
        os.remove(test_file)
    except Exception:
        print("  ❌ Internal Flash Storage  : WRITE ABORTED (Permissions Restricted)")

    bat = get_battery_metrics()
    print(f"  ✓ Battery Fuel Gauge      : {bat['capacity']} ({bat['status']})")
    print(f"  ✓ Power Matrix Core Temp  : {bat['temp']}")

    return {"battery_cap": bat["capacity"], "battery_temp": bat["temp"]}
