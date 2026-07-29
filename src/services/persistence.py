"""
Persistence Service for Termux-Doctor.

Handles serializing and deserializing diagnostic reports and sessions
for historical analysis.
"""

import json
import os
from datetime import datetime
from typing import Any


class PersistenceService:
    """Handles saving and loading diagnostic data."""

    def __init__(self, storage_dir: str = "reports/"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save_report(self, report_data: dict[str, Any], name: str | None = None) -> str:
        """Persists a diagnostic report to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name or 'report'}_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)

        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)
        return filepath

    def load_report(self, filename: str) -> dict[str, Any]:
        """Loads a report from file."""
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath) as f:
            return json.load(f)

    def list_reports(self) -> list[str]:
        """Lists available reports."""
        return [f for f in os.listdir(self.storage_dir) if f.endswith(".json")]
