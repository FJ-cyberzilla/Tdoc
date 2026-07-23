# TDoc Platform Diagnostics

TDoc is a hardened, service-oriented diagnostic platform designed for Termux environments. It provides comprehensive system health, environment, network, and security auditing with a modern terminal-based UI.

## Architecture

TDoc is built on a modular, service-oriented architecture:

*   **Orchestrator Layer (`router.py`)**: Centralized routing of diagnostic requests via dependency injection.
*   **Service Layer (`advanced/`)**: Independent diagnostic services implementing the `DiagnosticService` interface.
*   **UI Layer (`ui_manager.py`, `theme.py`)**: Decoupled rendering engine using `Rich` for clean, themeable output.
*   **Integrity Layer (`updater.py`)**: Automated workspace and dependency validation.

## Diagnostic Services

*   **PlatformService**: Aggregates environment (OS, Android properties) and hardware health (battery, storage) data.
*   **NetworkService**: Validates global connectivity, detects VPN drag, and audits local socket availability.
*   **SecurityService**: Performs host privilege audits, SELinux status checks, and detects potential LD_PRELOAD injection vectors.
*   **UpdaterService**: Validates repository integrity and Git synchronization status.

## Key Principles

*   **Fail-Fast**: Robust error handling via specific exceptions (`TDocError`, `UIError`).
*   **Composition**: Usage of composite services (`PlatformService`) for clean functionality aggregation.
*   **Security-First**: No OWASP vulnerabilities; strict isolation of system binary calls.
*   **Testability**: Every service is designed for isolated unit testing.

## Usage

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Start the HUD
python main.py
```

## Contributing

Please adhere to the project's coding standards defined in `GEMINI.md`. All contributions must pass `make lint` (Ruff) and include corresponding unit tests.
