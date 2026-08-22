# Termux-Doctor User Guide

Welcome to the official user guide for Termux-Doctor (TDoc), the comprehensive diagnostic suite for the Termux ecosystem.
## 1. Getting Started
### Installation
TDoc relies on `uv` for dependency management and system orchestration.
```bash
# Clone the repository
git clone https://github.com/FJ-cyberzilla/Termux-Doctor.git
cd Termux-Doctor

# Initialize system and dependencies
make install
```

### Quick Start
To launch the diagnostic HUD:
```bash
make run
```

## 2. Command Reference
TDoc uses a comprehensive `Makefile` to orchestrate tasks. Available commands:

| Command | Description |
| :--- | :--- |
| `make build` | Build Python package |
| `make check-deps` | Audit presence of uv and utilities |
| `make clean` | Flush bytecode, cache, and venv |
| `make diagnose` | Linting & structural checks |
| `make format` | Auto-format Python code via ruff |
| `make install` | Setup system & dependencies via uv |
| `make lint` | Run Ruff static code analysis |
| `make pack-install` | Register global 'tdoc' execution alias |
| `make run` | Boot the interactive telemetry HUD |
| `make sync` | Synchronize project dependencies |
| `make test` | Execute test suite via pytest |
| `make update` | Robust project update |

## 3. Features
...
- **Telemetry Dashboard**: Real-time monitoring of system metrics (CPU, RAM, Battery).
- **Network Deep-Dive**: Connectivity checks, DNS leak detection, and hotspot monitoring.
- **Security Audit**: Automated scanning for SUID anomalies, SELinux status, and root integrity.
- **Smart Sensor Hub**: Automatically detects and queries supported device sensors (Accelerometer, Light, Gyroscope, Magnetometer, Hall IC). If a sensor is unavailable, it is gracefully marked as "NOT DETECTED" instead of returning invalid data.
- **Tactile Alerts (Haptic Feedback)**: Provides vibration feedback for high-intensity sensor anomalies, such as significant magnetic field presence. This feature can be enabled/disabled programmatically via the SensorHubService instance.

## 3. Configuration
TDoc supports customization via `config.json`.
- **Thresholds**: Override diagnostic thresholds (e.g., battery alerts, network latency timeouts).
- **Paths**: Adjust report storage locations.

## 4. Advanced Usage & Persistence
TDoc automatically persists diagnostic reports and session logs to `reports/`. Use these logs to track system health trends over time.

## 5. Troubleshooting & FAQ
- **Tools failing?**: Ensure `termux-api` package is installed on your device (`pkg install termux-api`).
- **Permission errors?**: Grant storage access to Termux (`termux-setup-storage`).
- **Still having issues?**: Report issues on our GitHub repository.
