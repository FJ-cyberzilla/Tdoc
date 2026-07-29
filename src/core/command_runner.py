"""
Command Runner utility for executing system commands safely.
"""

import logging
import subprocess

logger = logging.getLogger(__name__)


class CommandRunner:
    """Provides safe execution and basic parsing of system commands."""

    @staticmethod
    def run_command(command: list[str]) -> str:
        """Executes a command and returns the stdout."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)} - {e.stderr}")
            return ""
        except FileNotFoundError:
            logger.error(f"Command not found: {command[0]}")
            return ""

    @staticmethod
    def parse_key_value(output: str, delimiter: str = ":") -> dict:
        """Parses simple key-value pairs from command output."""
        data = {}
        for line in output.splitlines():
            if delimiter in line:
                key, value = line.split(delimiter, 1)
                data[key.strip()] = value.strip()
        return data
