# Android System Query Commands

This document lists comprehensive commands and techniques to retrieve system, hardware, and diagnostic information from Android devices via Termux. These commands are essential for data collection features in Termux-Doctor.

## 1. System Commands

### Device & Hardware
```bash
getprop                    # ALL system properties
getprop ro.product.model   # Device model
getprop ro.product.manufacturer  # Manufacturer
getprop ro.build.version.release  # Android version
getprop ro.hardware        # Hardware platform
getprop ro.board.platform  # SoC platform
cat /proc/cpuinfo         # CPU details
cat /proc/meminfo         # Memory info
cat /proc/partitions      # Partitions
df -h                     # Storage usage
lsblk                     # Block devices
free -h                   # RAM usage
uptime                    # System uptime
uname -a                  # Kernel info
```

### Network
```bash
ip addr                  # All network interfaces
ip link                  # Network links
ip route                 # Routing table
ifconfig -a             # Interface configs
netstat -tulpn          # Open ports
ss -tulpn               # Socket stats
cat /proc/net/dev       # Network statistics
cat /proc/net/tcp       # TCP connections
ping -c 4 8.8.8.8       # Connectivity test
traceroute google.com   # Route trace
nslookup google.com     # DNS lookup
dig google.com          # DNS details
```

### Processes & System
```bash
ps aux                  # All processes
top -n 1                # Process list
pstree                  # Process tree
systemctl list-units    # Services (if available)
cat /proc/loadavg      # System load
cat /proc/uptime       # Uptime seconds
dmesg | tail -50       # Kernel messages
logcat -d              # System log
who                    # Logged in users
last                   # Login history
```

## 2. Android Specific (`dumpsys`)

### Core System
`dumpsys -l`, `dumpsys activity`, `dumpsys package`, `dumpsys meminfo`, `dumpsys cpuinfo`, `dumpsys diskstats`, `dumpsys battery`, `dumpsys power`, `dumpsys deviceidle`, `dumpsys thermalservice`.

### Network & Telephony
`dumpsys connectivity`, `dumpsys wifi`, `dumpsys netstats`, `dumpsys telephony.registry`, `dumpsys phone`, `dumpsys simphonebook`, `dumpsys bluetooth_manager`, `dumpsys nfc`.

### Sensors & Hardware
`dumpsys sensorservice`, `dumpsys display`, `dumpsys window`, `dumpsys input`, `dumpsys gps`, `dumpsys location`, `dumpsys audio`, `dumpsys media`, `dumpsys camera`.

### Security & Permissions
`dumpsys device_policy`, `dumpsys permission`, `dumpsys account`, `dumpsys usagestats`, `dumpsys battery_stats`.

## 3. Termux API Commands

*Note: Requires `termux-api` package.*

```bash
termux-telephony-deviceinfo   # Complete device/network info
termux-telephony-cellinfo     # Cell tower info
termux-telephony-signalstrength  # Signal strength
termux-wifi-connectioninfo    # WiFi connection details
termux-wifi-scaninfo          # WiFi scan results
termux-battery-status         # Battery status
termux-sensor                 # Sensor readings
termux-location               # GPS location
termux-camera-info            # Camera info
termux-microphone-info        # Microphone info
termux-speaker-info           # Speaker info
termux-clipboard-get          # Clipboard content
termux-notification-list      # Notifications
```

## 4. `/sys` Filesystem (Real-time Hardware)

*   **CPU:** `/sys/devices/system/cpu/...`
*   **Memory:** `/sys/fs/cgroup/memory/...`
*   **Battery:** `/sys/class/power_supply/battery/...`
*   **Sensors:** `/sys/class/sensors/...`, `/sys/class/accel/...`, `/sys/class/gyro/...`, etc.
*   **Storage:** `/sys/block/...`
*   **Network:** `/sys/class/net/...`
*   **Display:** `/sys/class/graphics/...`, `/sys/class/backlight/...`
*   **USB:** `/sys/bus/usb/devices/...`

## 5. Recommended Packages

```bash
pkg install termux-api termux-tools python busybox net-tools procps util-linux dnsutils traceroute nmap htop tree openssh rsync wget curl jq ncdu sysstat
```
