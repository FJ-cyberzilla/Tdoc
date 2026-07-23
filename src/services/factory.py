"""
Service Factory
"""

from typing import Dict, Any
from src.services.platform import PlatformService
from src.services.network import NetworkService
from src.services.security import SecurityService
from src.services.updater import UpdaterService
from src.services.health import HealthService
from src.services.package_manager import PackageManagerService
from src.services.utility import UtilityService


class ServiceFactory:
    """Factory to manage service instantiation."""

    @staticmethod
    def get_services() -> Dict[str, Any]:
        """Returns a dictionary of initialized services."""
        return {
            "platform": PlatformService(),
            "network": NetworkService(),
            "security": SecurityService(),
            "updater": UpdaterService(),
            "health": HealthService(),
            "package_manager": PackageManagerService(),
            "utility": UtilityService(),
        }
