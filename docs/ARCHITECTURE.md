# Termux-Doctor Architecture

Termux-Doctor (TDoc) is built to be a robust, extensible diagnostic suite for Termux. This document outlines the system architecture, component design, and extensibility patterns.

## 1. System Overview
TDoc follows a modular, layered architecture that separates diagnostic logic, UI presentation, and configuration management.

- **CLI/Router Layer (`cmd/tdoc/`)**: Central orchestration for all diagnostic requests.
- **Service Layer (`internal/services/`)**: Independent diagnostic modules (e.g., Network, Security, Battery).
- **Models Layer (`internal/models/`)**: Data structures and system interface definitions.
- **UI Layer (`internal/ui/`)**: Terminal HUD for rendering results with controller handling.
- **Cache Layer (`internal/cache/`)**: Shared helpers and robust data management.

## 2. Component Interaction
1. **Request**: UI triggers a diagnostic task via the CLI handler.
2. **Dispatch**: Router dispatches to the appropriate `Service`.
3. **Execution**: `Service` executes diagnostics, leveraging the `Models` for shared I/O interface.
4. **Persistence**: Results are optionally persisted via `cache` if configured.
5. **Display**: Results are returned to the `UI` controller, which renders them.

## 3. Extensibility: Adding a New Service
To add a new diagnostic service:
1. Create a new file in `internal/services/` (or subdirectory).
2. Implement the diagnostic logic, ensuring robust error handling.
3. Register the service in the main orchestration flow.

## 4. Configuration & Persistence
- **Configuration**: Managed by `config.json` at the project root.
- **Persistence**: Managed by the cache layer to save and load diagnostic reports, enabling historical trend analysis.
