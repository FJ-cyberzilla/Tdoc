"""
Configuration Service for Termux-Doctor.

Provides centralized management of tool settings, check thresholds,
and platform-specific parameters.
"""

import json
import os
from typing import Any


class ConfigService:
    """Handles loading, saving, and accessing project configuration."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Loads configuration from file or initializes defaults."""
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                self.config = json.load(f)
        else:
            self.config = self._get_defaults()
            self.save_config()

    def _get_defaults(self) -> dict[str, Any]:
        """Returns default configuration values."""
        return {
            "check_thresholds": {
                "battery_low": 20,
                "storage_warning": 10,  # GB
            },
            "ui_settings": {"theme": "default"},
        }

    def save_config(self):
        """Persists current configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Sets a configuration value and persists it."""
        self.config[key] = value
        self.save_config()
