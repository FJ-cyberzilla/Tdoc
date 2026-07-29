# Termux-Doctor User Guide

Welcome to the official user guide for Termux-Doctor (TDoc), the comprehensive diagnostic suite for the Termux ecosystem.

## 1. Getting Started
### Installation
Ensure you have Python installed in your Termux environment.
```bash
pip install tdoc
```

### Quick Start
Execute the diagnostic tool from your terminal:
```bash
tdoc
```

## 2. Features
- **Telemetry Dashboard**: Real-time monitoring of system metrics (CPU, RAM, Battery).
- **Network Deep-Dive**: Connectivity checks, DNS leak detection, and hotspot monitoring.
- **Security Audit**: Automated scanning for SUID anomalies, SELinux status, and root integrity.

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
