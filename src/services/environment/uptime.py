import re
import subprocess
import time


class UptimeCollector:
    """Collects system uptime information."""

    def get_uptime(self) -> str:
        """Parses /proc/uptime for system uptime."""
        # 1. Try `uptime` command first
        uptime_cmd = self._get_uptime_from_command()
        if uptime_cmd:
            return uptime_cmd

        # 2. Fallback to /proc/uptime
        uptime_proc = self._get_uptime_from_proc()
        if uptime_proc:
            return uptime_proc

        # 3. Last effort fallback to uptime calculation
        uptime_calc = self._get_uptime_from_calc()
        if uptime_calc:
            return uptime_calc

        return "Uptime unavailable"

    def _get_uptime_from_command(self) -> str | None:
        try:
            output: str = subprocess.check_output(["uptime"], text=True)
            match = re.search(r"up\s+(.*?)(?:,|\s+user)", output)
            return match.group(1).strip() if match else None
        except Exception:
            return None

    def _get_uptime_from_proc(self) -> str | None:
        try:
            with open("/proc/uptime") as f:
                seconds: float = float(f.read().split()[0])
                return self._format_seconds_to_uptime(seconds)
        except Exception:
            return None

    def _format_seconds_to_uptime(self, seconds: float) -> str:
        days: int = int(seconds // 86400)
        hours: int = int((seconds % 86400) // 3600)
        minutes: int = int((seconds % 3600) // 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        return " ".join(parts) if parts else "Just started"

    def _get_uptime_from_calc(self) -> str | None:
        try:
            boot_time = (
                int(subprocess.check_output(["getprop", "ro.boottime.init"], text=True).strip())
                / 1000
            )
            uptime_seconds = time.time() - boot_time
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        except Exception:
            return None
