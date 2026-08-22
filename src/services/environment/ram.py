class RAMCollector:
    """Collects RAM information."""

    def get_ram_info(self) -> dict[str, float]:
        """Parses /proc/meminfo for RAM metrics in GB."""
        ram: dict[str, float] = {"total": 0.0, "available": 0.0, "used": 0.0, "percent": 0.0}
        try:
            meminfo = self._parse_meminfo()
            total: int = meminfo.get("MemTotal", 0)
            available: int = meminfo.get("MemAvailable", meminfo.get("MemFree", 0))

            if total > 0:
                ram["total"] = total / (1024 * 1024)  # GB
                ram["available"] = available / (1024 * 1024)  # GB
                ram["used"] = ram["total"] - ram["available"]
                ram["percent"] = (ram["used"] / ram["total"]) * 100
        except Exception:
            pass
        return ram

    def _parse_meminfo(self) -> dict[str, int]:
        """Parses /proc/meminfo into a dictionary."""
        meminfo: dict[str, int] = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    name: str = parts[0].strip()
                    value: int = int(parts[1].split()[0].strip())
                    meminfo[name] = value
        return meminfo
