"""
TDoc Security Subsystem – Hardened Privilege Audit
"""

import os
import stat
import subprocess


def check_root_presence() -> tuple:
    """
    Verifies existence and privilege status of common 'su' binaries.
    Returns (bool, str).
    """
    su_paths = [
        "/system/bin/su",
        "/system/xbin/su",
        "/sbin/su",
        "/usr/bin/su",
        "/su/bin/su",
        "/data/adb/magisk/su",
    ]
    found_nonsetuid = []
    errors = []

    for path in su_paths:
        try:
            st = os.stat(path)
            if not stat.S_ISREG(st.st_mode):
                continue
            if st.st_mode & stat.S_ISUID:
                return True, f"DETECTED – setuid root at {path}"
            found_nonsetuid.append(path)
        except FileNotFoundError:
            continue
        except PermissionError:
            errors.append(f"{path} (permission denied)")
        except Exception as e:
            errors.append(f"{path} ({e})")

    if found_nonsetuid:
        return False, f"Found but NO setuid bit: {', '.join(found_nonsetuid)}"
    if errors:
        return False, f"Could not read all paths: {'; '.join(errors)}"
    return False, "PRISTINE (No su binary found)"


def check_selinux_status() -> str:
    """
    Reads actual SELinux enforcement status.
    Returns a descriptive string.
    """
    status = None

    # Method 1: read directly from selinuxfs
    enforce_path = "/sys/fs/selinux/enforce"
    try:
        with open(enforce_path, "r", encoding="utf-8") as f:
            val = f.read().strip()
            if val == "1":
                status = "Enforcing (Strict Sandbox active)"
            elif val == "0":
                status = "Permissive (SELinux is loaded but not enforcing)"
            else:
                status = f"Unknown SELinux state (enforce file: {val})"
    except (FileNotFoundError, PermissionError):
        pass
    except Exception:
        pass

    if status is not None:
        return status

    # Method 2: use getenforce command
    try:
        out = subprocess.check_output(
            ["getenforce"], stderr=subprocess.DEVNULL, timeout=2
        )
        out_status = out.decode().strip()
        if out_status == "Enforcing":
            status = "Enforcing (Strict Sandbox active)"
        elif out_status == "Permissive":
            status = "Permissive (SELinux is loaded but not enforcing)"
        elif out_status == "Disabled":
            status = "Disabled (SELinux not loaded)"
        else:
            status = f"SELinux status: {out_status}"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    except Exception:
        pass

    if status is not None:
        return status

    # Method 3: check if selinuxfs is mounted
    try:
        mounts = subprocess.check_output(
            ["mount"], stderr=subprocess.DEVNULL, timeout=2
        ).decode()
        if "selinuxfs" in mounts:
            status = "SELinux filesystem mounted but state unknown"
    except Exception:
        pass

    if status is not None:
        return status

    return "SELinux not detected (could not determine status)"


def check_ld_preload() -> tuple:
    """
    Evaluates LD_PRELOAD variable, splits into components,
    and checks for trusted Termux libraries.
    Returns (is_active: bool, message: str).
    """
    preload = os.environ.get("LD_PRELOAD", "").strip()
    if not preload:
        return False, "INACTIVE (No preloaded injection vectors)"

    parts = preload.replace(" ", ":").split(":")
    parts = [p for p in parts if p]

    termux_libs = {"libtermux-exec.so", "libtermux.so"}
    trusted = []
    external = []
    for lib in parts:
        base = os.path.basename(lib)
        if base in termux_libs:
            trusted.append(lib)
        else:
            external.append(lib)

    if trusted and not external:
        return True, f"ACTIVE (Trusted Termux Core: {', '.join(trusted)})"
    if trusted and external:
        return (
            True,
            f"ACTIVE – Mixed (Trusted: {', '.join(trusted)} | External: {', '.join(external)})",
        )
    return True, f"ACTIVE – External Hook(s): {', '.join(external)}"


def check_termux_suid_binaries() -> str:
    """
    Scans the Termux prefix binary directory for files with setuid/setgid bits.
    """
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    bin_dir = os.path.join(prefix, "bin")
    if not os.path.isdir(bin_dir):
        return f"PREFIX/bin not found ({bin_dir})"

    suid_found = []
    try:
        for entry in os.scandir(bin_dir):
            if entry.is_file(follow_symlinks=False):
                try:
                    st = entry.stat()
                    if st.st_mode & (stat.S_ISUID | stat.S_ISGID):
                        suid_found.append(entry.name)
                except (PermissionError, OSError):
                    pass
    except PermissionError:
        return "Permission denied scanning PREFIX/bin"

    if suid_found:
        return f"WARNING – SUID/SGID binaries found: {', '.join(suid_found)}"
    return "Pristine (No local SUID anomalies)"


def run_security_checks() -> dict:
    """Executes host privilege security audit with real system inspection."""
    has_root, root_msg = check_root_presence()
    selinux_status = check_selinux_status()
    ld_active, ld_msg = check_ld_preload()
    suid_msg = check_termux_suid_binaries()

    return {
        "root_presence": {"found": has_root, "message": root_msg},
        "selinux": selinux_status,
        "ld_preload": {"active": ld_active, "message": ld_msg},
        "termux_suid": suid_msg,
    }
