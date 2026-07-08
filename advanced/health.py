import time
"""
TDoc Command Center - System Health & Hardware Infrastructure
"""

import os
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.theme import Theme
from constants import ORANGE_THEME, PREFIX
from helper import run_pure_command

console = Console(theme=Theme(ORANGE_THEME))

def get_cpu_and_mem_usage() -> Dict[str, Any]:
    """Parses /proc system tables directly to map core hardware usage metrics."""
    stats = {"cpu": "Unknown", "mem_free_mb": 0}
    
    # Process Memory Audit
    mem_info = Path("/proc/meminfo")
    if mem_info.is_file():
        lines = mem_info.read_text().splitlines()
        mem_total = 0
        mem_available = 0
        for line in lines:
            if "MemTotal" in line:
                mem_total = int(line.split()[1])
            if "MemAvailable" in line:
                mem_available = int(line.split()[1])
        
        if mem_total > 0:
            used_pct = ((mem_total - mem_available) / mem_total) * 100
            stats["mem_free_mb"] = mem_available // 1024
            console.print(f"  [status.optimal]✓[/status.optimal] Memory Overhead: [text.primary]{used_pct:.1f}% used[/text.primary] ({stats['mem_free_mb']} MB Available)")
            
    return stats

def run_storage_io_benchmark() -> float:
    """Benchmarks local filesystem write performance safely inside the Termux sandbox."""
    test_file = Path(PREFIX) / "tmp" / "tdoc_io.tst"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    payload = b"0" * 1024 * 1024 * 10  # 10MB test payload
    start = time.monotonic()
    try:
        test_file.write_bytes(payload)
        duration = time.monotonic() - start
        test_file.unlink()
        io_speed = 10.0 / duration
        console.print(f"  [status.optimal]✓[/status.optimal] Internal Flash Storage Write Speed: [text.primary]{io_speed:.2f} MB/s[/text.primary]")
        return io_speed
    except OSError:
        console.print("  [status.critical]✗ Filesystem I/O benchmark aborted (Permission Denied)[/status.critical]")
        return -1.0

def read_thermal_zones() -> None:
    """Traverses kernel thermal boundaries to identify silicon throttling bottlenecks."""
    thermal_dir = Path("/sys/class/thermal")
    found_sensor = False
    
    if thermal_dir.is_dir():
        for zone in thermal_dir.glob("thermal_zone*"):
            try:
                temp = int((zone / "temp").read_text().strip()) / 1000
                type_str = (zone / "type").read_text().strip()
                if temp > 0:
                    console.print(f"  [status.optimal]✓[/status.optimal] Sensor [text.muted]{type_str}[/text.muted]: {temp:.1f}°C")
                    found_sensor = True
                    break # Single clean printout is sufficient for the summary interface
            except (OSError, ValueError):
                continue
                
    if not found_sensor:
        console.print("  [status.warning]▪ Thermal Matrix Restricted:[/status.warning] Device hardware layers are obfuscated.")
