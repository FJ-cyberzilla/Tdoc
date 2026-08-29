"""
Configuration Service for Termux-Doctor.

Provides centralized management of tool settings, check thresholds,
and platform-specific parameters.
"""

import json
import os
from typing import TypedDict, cast


class Thresholds(TypedDict):
    battery_low: int
    storage_warning: int


class UISettings(TypedDict):
    theme: str


class Config(TypedDict):
    check_thresholds: Thresholds
    ui_settings: UISettings


class ConfigService:
    """Handles loading, saving, and accessing project configuration."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.config: Config = cast(Config, {})
        self._load_config()

    def _load_config(self) -> None:
        """Loads configuration from file or initializes defaults."""
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                data = json.load(f)
                self.config = self._validate_and_convert(data)
        else:
            self.config = self._get_defaults()
            self.save_config()

    def _validate_and_convert(self, data: object) -> Config:
        """Validates loaded configuration structure."""
        if not isinstance(data, dict):
            raise ValueError("Invalid config format")

        d_data = cast(dict[str, object], data)

        if "check_thresholds" not in d_data or "ui_settings" not in d_data:
            raise ValueError("Invalid config keys")

        check_thresholds = d_data["check_thresholds"]
        ui_settings = d_data["ui_settings"]

        if not isinstance(check_thresholds, dict) or not isinstance(ui_settings, dict):
            raise ValueError("Invalid config structure")

        d_thresholds = cast(dict[str, object], check_thresholds)
        d_ui = cast(dict[str, object], ui_settings)

        # Validate Thresholds
        if "battery_low" not in d_thresholds or not isinstance(d_thresholds["battery_low"], int) or \
           "storage_warning" not in d_thresholds or not isinstance(d_thresholds["storage_warning"], int):
            raise ValueError("Invalid threshold values")

        # Validate UISettings
        if "theme" not in d_ui or not isinstance(d_ui["theme"], str):
            raise ValueError("Invalid UI settings")

        return cast(Config, data)

    def _get_defaults(self) -> Config:
        """Returns default configuration values."""
        return {
            "check_thresholds": {
                "battery_low": 20,
                "storage_warning": 10,  # GB
            },
            "ui_settings": {"theme": "default"},
        }

    def save_config(self) -> None:
        """Persists current configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_thresholds(self) -> Thresholds:
        """Retrieves threshold settings."""
        return self.config["check_thresholds"]

    def get_ui_settings(self) -> UISettings:
        """Retrieves UI settings."""
        return self.config["ui_settings"]
