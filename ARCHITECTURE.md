# Termux-Doctor Architecture

Termux-Doctor (TDoc) is built to be a robust, extensible diagnostic suite for Termux. This document outlines the system architecture, component design, and extensibility patterns.

## 1. System Overview
TDoc follows a modular, layered architecture that separates diagnostic logic, UI presentation, and configuration management.

- **API/Router Layer (`src/router.py`)**: Central orchestration for all diagnostic requests.
- **Service Layer (`src/services/`)**: Independent diagnostic modules (e.g., Network, Security, Battery).
- **Core Layer (`src/core/`)**: High-performance engine, theme, and service coordination.
- **UI Layer (`src/ui/`)**: MVC-pattern terminal HUD for rendering results.
- **Utility Layer (`src/utils/`)**: Shared helpers, robustness utilities, and report serialization.

## 2. Component Interaction
1. **Request**: UI triggers a diagnostic task via the `Router`.
2. **Dispatch**: `Router` dispatches to the appropriate `Service`.
3. **Execution**: `Service` executes diagnostics, leveraging the `Core Engine` for shared I/O.
4. **Persistence**: Results are optionally persisted via `PersistenceService` if configured.
5. **Display**: Results are returned to the `UI` controller, which renders them via the `Renderer`.

## 3. Extensibility: Adding a New Service
To add a new diagnostic service:
1. Create a new file in `src/services/`.
2. Implement the diagnostic logic, ensuring robust error handling using the `retry` decorator from `src/utils/robustness.py`.
3. Register the service in `src/services/factory.py`.

## 4. Configuration & Persistence
- **Configuration**: Managed by `ConfigService`, allowing threshold overrides and setting adjustments.
- **Persistence**: Managed by `PersistenceService` to save and load diagnostic reports, enabling historical trend analysis.
