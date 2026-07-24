# TDoc :: Platform Matrix
*SOTA Termux System Integrity Diagnostics & Control HUD*

### https://fj-cyberzilla.github.io/Tdoc/
---

## ⚡ Overview
TDoc is a hardened, modular diagnostic suite designed specifically for the Termux environment. It provides real-time monitoring of system health, network topology, security auditing, and workspace synchronization, all presented through an aesthetic terminal HUD.

## 🏗️ Architectural Core
The system follows a strict modular architecture to ensure security, maintainability, and extensibility:

- **CLI Interface (`main.py`)**: The central entry gate, handling the security sandbox and application lifecycle.
- **HUD Layer (`ui/`)**: A reactive, theme-based UI layer rendering terminal panels using `rich`.
- **Orchestrator (`router.py`)**: A centralized routing layer decoupling the UI from system logic via the `TDocRouter`.
- **Service Layer (`services/`)**: Focused, single-responsibility components managing:
    - **Platform**: Hardware metrics, storage, environment.
    - **Network**: Topology mapping, VPN detection, mirror health.
    - **Security**: Audit of SUID, root, and SELinux posture.
    - **Package Manager**: Efficient inventory of installed binaries.
    - **Utility**: On-demand installation and execution of external tools (`htop`, `neofetch`).

## 🚀 Operations
The project uses `uv` for deterministic dependency management and includes a comprehensive `Makefile` for orchestration.

### Key Targets:
| Command | Action |
| :--- | :--- |
| `make install` | Boots infrastructure and dependencies. |
| `make run` | Starts the interactive telemetry HUD. |
| `make lint` | Runs `ruff` static analysis. |
| `make diagnose` | Full health audit (Lint + Structural footprint). |
| `make clean` | Purges caches and build artifacts. |

## 🛠️ Usage
1. Initialize: `make install`
2. Run: `make run`
3. Navigate: Use the main menu to route diagnostics.

---
*Developed for FJ™ Cybertronic Systems.*
