"""
TDoc Command Center - Global Constants and Visual Palettes
"""

import os
from pathlib import Path

# Termux Environment Boundaries
PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
HOME = os.environ.get("HOME", "/data/data/com.termux/files/home")

# Ports to scan for active/suspicious internal listeners
SCAN_PORTS = [22, 80, 443, 1080, 3000, 5000, 8000, 8080, 9000, 9050, 9150]

# High-reliability targets for network validation
CHECK_SITES = [
    {"name": "Cloudflare DNS", "url": "https://1.1.1.1", "type": "local"},
    {"name": "Google Core", "url": "https://www.google.com", "type": "local"},
    {"name": "GitHub API", "url": "https://api.github.com", "type": "intl"},
    {"name": "Termux Main", "url": "https://packages.termux.org", "type": "intl"},
]

DNS_PROVIDERS = [
    ("Cloudflare", "1.1.1.1"),
    ("Google", "8.8.8.8"),
    ("Quad9", "9.9.9.9"),
    ("NextDNS", "45.90.28.0"),
]

TERMUX_MIRRORS = [
    ("Main Pool", "https://packages.termux.dev/apt/termux-main"),
    ("Grimler Mirror", "https://termux.grimler.se/termux-main"),
    ("Tsinghua OS", "https://mirrors.tuna.tsinghua.edu.cn/termux/termux-main"),
]

# SOTA Command Center Orange Spectrum Styles
ORANGE_THEME = {
    "status.critical": "bold #FF3D00",  # Neon Red-Orange
    "status.warning": "bold #FF9100",   # Bright Amber-Orange
    "status.optimal": "bold #00E676",   # Contrasting Alert Green
    "panel.border": "#FF6D00",          # Deep Safety Orange
    "text.primary": "#FFAB40",           # Soft Command Text Orange
    "text.muted": "#FFD180",             # Pale Highlight Orange
    "banner": "bold #FF6D00",
}
