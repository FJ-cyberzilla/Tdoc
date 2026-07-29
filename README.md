# Termux-Doctor (TDoc)

[![Version](https://img.shields.io/badge/version-5.4.9-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Termux-Doctor is a high-performance diagnostic suite designed specifically for the Termux ecosystem. It provides advanced system integrity diagnostics, real-time telemetry, and automated security auditing in a unified control HUD.

## Features
- **Telemetry Dashboard**: Monitor CPU, RAM, and Battery status in real-time.
- **Network Deep-Dive**: DNS leak detection, latency analysis, and hotspot monitoring.
- **Security Audit**: Root detection, SELinux status, and SUID anomaly scanning.
- **Extensible Architecture**: Easily add custom diagnostic services.

## Quick Start
```bash
# Clone the repository
git clone https://github.com/FJ-cyberzilla/Termux-Doctor.git
cd Termux-Doctor

# Initialize environment
make install

# Boot the telemetry HUD
make run
```

## Documentation
- **[User Guide](USER_GUIDE.md)**: Detailed usage, configuration, and troubleshooting.
- **[Architecture](ARCHITECTURE.md)**: System design and extensibility guide.
- **[Development Guide](DEVELOPMENT.md)**: Coding standards, testing, and contribution workflow.

## License
TDoc is licensed under the MIT License. See [LICENSE](LICENSE) for details.
