"""
TDoc Security Subsystem - Root Isolation & Privilege Hijack Detection Traps
"""

import os
import subprocess

def run_security_checks() -> dict:
    """Executes structural integrity scans across environment isolation boundaries."""
    print("\n🛡 --- [ PRIVACY & HOST PRIVILEGE SECURITY ] ---")

    # 1. Root / SU Binary Presence Cross-Check
    root_paths = [
        "/system/bin/su", "/system/xbin/su", "/sbin/su",
        "/su/bin/su", "/data/local/xbin/su", "/data/local/bin/su"
    ]
    is_rooted = any(os.path.exists(path) for path in root_paths)

    try:
        binary_lookup = subprocess.run(
            ["which", "su"], capture_output=True, text=True, check=False
        )
        if binary_lookup.returncode == 0:
            is_rooted = True
    except Exception:
        pass

    if is_rooted:
        print("  ⚠️  Root Binary Presence: DETECTED (System environment boundaries modified)")
    else:
        print("  ✓ Root Binary Presence: UNDETECTED (Standard sandbox containment intact)")

    # 2. SELinux Containment State Audit
    selinux_status = "Enforcing"
    try:
        if os.path.exists("/sys/fs/selinux/enforce"):
            with open("/sys/fs/selinux/enforce", "r") as state_file:
                if state_file.read().strip() == "0":
                    selinux_status = "Permissive (Isolation Lowered)"
        else:
            system_check = subprocess.run(
                ["getenforce"], capture_output=True, text=True, check=False
            )
            if system_check.returncode == 0:
                selinux_status = system_check.stdout.strip()
    except Exception:
        selinux_status = "Unknown (Obfuscated Layers)"

    if "Permissive" in selinux_status or "Disabled" in selinux_status:
        print(f"  ⚠️  SELinux Isolation State: {selinux_status} (High Privilege Risk)")
    else:
        print(f"  ✓ SELinux Isolation State: {selinux_status} (Strict App Sandbox active)")

    # 3. Memory Injection Hijack Vectors
    ld_preload = os.environ.get("LD_PRELOAD")
    if ld_preload:
        print(f"  ⚠️  Injection Hijack Vector: LD_PRELOAD Active -> {ld_preload[:45]}")
    else:
        print("  ✓ Injection Hijack Vector: Clean (No dynamic runtime hooks detected)")

    # 4. Termux Prefix SUID/SGID Privilege Trap Scan
    # Android filesystems mount storage nodes with 'nosuid' flags. Any compiled binary 
    # matching SUID/SGID bits inside a writable user terminal layout indicates exploit payloading.
    termux_prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    target_bin_dir = os.path.join(termux_prefix, "bin")
    suid_anomalies = []

    if os.path.exists(target_bin_dir):
        try:
            for node in os.listdir(target_bin_dir):
                full_path = os.path.join(target_bin_dir, node)
                if os.path.isfile(full_path) and not os.path.islink(full_path):
                    permissions = os.stat(full_path).st_mode
                    if (permissions & 0o4000) or (permissions & 0o2000):
                        suid_anomalies.append(node)
        except Exception:
            pass

    if suid_anomalies:
        print(f"  ❌ SUID/SGID Anomalies Found: {', '.join(suid_anomalies[:5])} (Privilege Trap!)")
    else:
        print("  ✓ Termux Binaries Isolation: Pristine (No local SUID/SGID anomalies structural)")

    return {
        "root_detected": is_rooted,
        "selinux_mode": selinux_status,
        "hijack_env_active": bool(ld_preload),
        "suid_traps_count": len(suid_anomalies)
    }
