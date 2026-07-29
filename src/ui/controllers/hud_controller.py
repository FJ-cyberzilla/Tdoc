"""
HUD Controller for Termux-Doctor.
Handles the main loop, input handling, and view-model updates.
"""

from src.core.dispatcher import CommandDispatcher
from src.core.theme import ThemeManager
from src.exceptions import TDocError
from src.ui.handlers import (
    DashboardHandler,
    NetworkHandler,
    PackageManagerHandler,
    SecurityHandler,
    SensorHandler,
    UpdaterHandler,
)
from src.ui.renderers.renderer import UIRenderer


class HUDController:
    """Manages the UI interaction loop."""

    def __init__(self, router, utility_service):
        self.router = router
        self.utility_service = utility_service
        self.theme = ThemeManager()
        self.renderer = UIRenderer(self.theme.console)
        self.dispatcher = CommandDispatcher(router, utility_service)
        self._register_commands()

    def _register_commands(self):
        """Registers commands to the dispatcher."""
        self.dispatcher.register_command(
            "1", "dashboard", DashboardHandler(self.renderer, self.router).handle
        )
        self.dispatcher.register_command(
            "2", "network", NetworkHandler(self.renderer, self.router).handle
        )
        self.dispatcher.register_command(
            "3", "security", SecurityHandler(self.renderer, self.router).handle
        )
        self.dispatcher.register_command(
            "4", "updater", UpdaterHandler(self.renderer, self.router).handle
        )
        self.dispatcher.register_command(
            "5", "package_manager", PackageManagerHandler(self.renderer, self.router).handle
        )
        self.dispatcher.register_command(
            "6", "htop", lambda _: self.utility_service.run_tool("htop")
        )
        self.dispatcher.register_command(
            "7", "neofetch", lambda _: self.utility_service.run_tool("neofetch")
        )
        self.dispatcher.register_command(
            "8", "sensor_hub", SensorHandler(self.renderer, self.router).handle
        )

    def start(self):
        """Runs the main UI interaction loop."""
        while True:
            self.renderer.clear_screen()
            self.renderer.render_header()
            self.renderer.render_navigation()

            try:
                # Rich console.input allows markup tags directly
                choice = self.theme.console.input(
                    "\n[accent.primary]▲[/] [text.muted]tdoc ⨠[/] "
                ).strip()
            except (KeyboardInterrupt, EOFError):
                self.theme.console.print("\n[text.muted]Session terminated by user.[/]")
                break

            if choice == "0":
                self.theme.console.print("\n[status.success]Diagnostic pipeline closed safely.[/]")
                break

            self._handle_choice(choice)
            self.theme.console.input("\n[text.muted]↵ Press Enter to return...[/]")

    def _handle_choice(self, choice: str):
        """Dispatches choices using the command dispatcher."""
        try:
            self.dispatcher.dispatch(choice)
        except ValueError:
            self.theme.console.print("\n[error.text] ✘ Invalid operation token [/]")
        except TDocError as e:
            self.theme.console.print(f"\n[error.text] ✘ {e.message} [/]")
            if e.context:
                self.theme.console.print(f"[text.muted]   Context: {e.context}[/]")
        except Exception as e:
            self.theme.console.print(f"\n[error.text] ✘ Unexpected exception: {e} [/]")
