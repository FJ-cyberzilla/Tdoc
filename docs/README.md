# Termux-Doctor Documentation

This directory contains technical documentation for the Termux-Doctor (TDoc) project.

## Project Overview
Termux-Doctor is a high-performance diagnostic suite designed specifically for the Termux ecosystem, providing advanced system integrity diagnostics, real-time telemetry, and automated security auditing in a unified control HUD.

## Documentation Structure
- **[Architecture](ARCHITECTURE.md)**: System design and extensibility guide.
- **[Development Guide](../DEVELOPMENT.md)**: Coding standards, testing, and contribution workflow.
- **[User Guide](../USER_GUIDE.md)**: Detailed usage, configuration, and troubleshooting.
- **[Android Commands](ANDROID_COMMANDS.md)**: Android-specific diagnostic techniques and tools.

## Key Architecture Components
- **Router**: Central orchestration layer.
- **Service Layer**: Independent diagnostic modules.
- **UI Layer**: MVC-pattern terminal HUD.
- **Persistence Layer**: Historical report management.
- **Robustness**: Transient failure management via retry decorators.

## Operations
The project uses `uv` for dependency management and `make` for task orchestration. Refer to the root `Makefile` for available commands.
