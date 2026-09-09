# Termux-Doctor User Guide

Welcome to the official user guide for Termux-Doctor (TDoc), the comprehensive diagnostic suite for the Termux ecosystem.

## 1. Getting Started
### Installation
To build Termux-Doctor from source:
```bash
# Clone the repository
git clone https://github.com/FJ-cyberzilla/Termux-Doctor.git
cd Termux-Doctor

# Build the project
make build
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
| `make build` | Compile the tdoc CLI |
| `make test` | Execute Go test suite |
| `make lint` | Run golangci-lint |
| `make vet` | Run go vet |
| `make run` | Build and execute tdoc |
| `make install` | Install tdoc to ~/.local/bin |
| `make clean` | Remove build artifacts |

## 3. Features
- **Telemetry Dashboard**: Real-time monitoring of system metrics (CPU, RAM, Battery).
- **Network Deep-Dive**: Connectivity checks, DNS leak detection, and hotspot monitoring.
- **Security Audit**: Automated scanning for SUID anomalies, SELinux status, and root integrity.
- **Smart Sensor Hub**: Automatically detects and queries supported device sensors.
- **Tactile Alerts**: Provides vibration feedback for high-intensity sensor anomalies.

## 4. Configuration
TDoc supports customization via `config.json` at the project root.

## 5. Troubleshooting & FAQ
- **Tools failing?**: Ensure `termux-api` package is installed on your device (`pkg install termux-api`).
- **Permission errors?**: Grant storage access to Termux (`termux-setup-storage`).
- **Still having issues?**: Report issues on our GitHub repository.
