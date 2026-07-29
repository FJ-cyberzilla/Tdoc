"""
Security check services for the Termux environment.

This module provides various checkers to verify the security state of the system,
including root presence, SELinux status, LD_PRELOAD injections, and SUID/SGID binaries.

Example usage:
    checker = RootPresenceChecker()
    result = checker.check()
    if result['found']:
        print(f"Alert: {result['message']}")
"""

import os
import stat
import subprocess
from typing import Any, Protocol

from src.exceptions import SecurityError


class SecurityChecker(Protocol):
    """Protocol defining the interface for security checker classes."""

    def check(self) -> dict[str, Any]:
        """
        Performs a security check and returns result data.

        Returns:
            dict[str, Any]: A dictionary containing the results of the check.
        """
        ...


class RootPresenceChecker:
    """
    Checks for the presence of 'su' binaries and setuid root bits.

    This checker scans common paths for the 'su' binary and verifies if it has
     the setuid bit set, which typically indicates a rooted device.
    """

    def check(self) -> dict[str, Any]:
        """
        Executes the root presence check.

        Returns:
            dict[str, Any]: Dictionary with 'found' (bool) and 'message' (str).
        """
        su_paths = [
            "/system/bin/su",
            "/system/xbin/su",
            "/sbin/su",
            "/usr/bin/su",
            "/su/bin/su",
            "/data/adb/magisk/su",
        ]

        found_nonsetuid, errors, setuid_found = self._scan_su_paths(su_paths)

        if setuid_found:
            return {"found": True, "message": f"DETECTED – setuid root at {setuid_found}"}

        return self._format_root_result(found_nonsetuid, errors)

    def _scan_su_paths(self, su_paths: list[str]) -> tuple[list[str], list[str], str | None]:
        """
        Scans a list of paths for su binaries.

        Args:
            su_paths: List of file paths to check.

        Returns:
            tuple: (found_nonsetuid, errors, setuid_found_path)
        """
        found_nonsetuid: list[str] = []
        errors: list[str] = []
        for path in su_paths:
            found_setuid = self._check_single_su_path(path, found_nonsetuid, errors)
            if found_setuid:
                return [], [], found_setuid
        return found_nonsetuid, errors, None

    def _check_single_su_path(
        self, path: str, found_nonsetuid: list[str], errors: list[str]
    ) -> str | None:
        """
        Analyzes a single path for su binary characteristics.

        Checks if the file exists, is a regular file, and has the setuid bit.
        """
        try:
            st = os.stat(path)
            # Ensure it's a regular file, not a directory or symlink
            if not stat.S_ISREG(st.st_mode):
                return None
            # Check for the setuid bit (typical for root su)
            if st.st_mode & stat.S_ISUID:
                return path
            found_nonsetuid.append(path)
        except (FileNotFoundError, PermissionError):
            # Normal if su is not present or inaccessible
            pass
        except Exception as e:
            raise SecurityError(f"Root check failed for {path}: {e}", context={"path": path}) from e
        return None

    def _format_root_result(self, found_nonsetuid: list[str], errors: list[str]) -> dict[str, Any]:
        """Formats the scan results into a user-friendly dictionary."""
        if found_nonsetuid:
            return {
                "found": False,
                "message": f"Found but NO setuid bit: {', '.join(found_nonsetuid)}",
            }
        if errors:
            return {"found": False, "message": f"Could not read all paths: {'; '.join(errors)}"}
        return {"found": False, "message": "PRISTINE (No su binary found)"}


class SELinuxStatusChecker:
    """
    Checks the current status of SELinux on the device.

    Tries multiple methods: checking /sys/fs/selinux/enforce, running 'getenforce',
    and checking mount points.
    """

    def check(self) -> dict[str, Any]:
        """
        Retrieves the SELinux status.

        Returns:
            dict[str, Any]: Dictionary with 'status' (str).
        """
        return {"status": self._get_status()}

    def _get_status(self) -> str:
        """Orchestrates different SELinux detection methods."""
        status = self._check_selinuxfs()
        if status:
            return status

        status = self._check_getenforce_cmd()
        if status:
            return status

        status = self._check_mounts()
        if status:
            return status

        return "SELinux not detected (could not determine status)"

    def _check_selinuxfs(self) -> str | None:
        """Checks the direct kernel interface for SELinux enforcement."""
        try:
            with open("/sys/fs/selinux/enforce", encoding="utf-8") as f:
                val = f.read().strip()
                if val == "1":
                    return "Enforcing (Strict Sandbox active)"
                if val == "0":
                    return "Permissive (SELinux is loaded but not enforcing)"
        except (FileNotFoundError, PermissionError):
            pass
        return None

    def _check_getenforce_cmd(self) -> str | None:
        """Attempts to run the 'getenforce' command line tool."""
        try:
            out = subprocess.check_output(["getenforce"], stderr=subprocess.DEVNULL, timeout=2)
            out_status = out.decode().strip()
            mapping = {
                "Enforcing": "Enforcing (Strict Sandbox active)",
                "Permissive": "Permissive (SELinux is loaded but not enforcing)",
                "Disabled": "Disabled (SELinux not loaded)",
            }
            return mapping.get(out_status)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return None

    def _check_mounts(self) -> str | None:
        """Checks the list of mounted filesystems for 'selinuxfs'."""
        try:
            mounts = subprocess.check_output(
                ["mount"], stderr=subprocess.DEVNULL, timeout=2
            ).decode()
            if "selinuxfs" in mounts:
                return "SELinux filesystem mounted but state unknown"
        except Exception:
            pass
        return None


class LDPreloadChecker:
    """
    Checks for LD_PRELOAD environment variable injections.

    LD_PRELOAD can be used to hook system calls and inject code into processes.
    This checker identifies trusted Termux libraries vs external ones.
    """

    def check(self) -> dict[str, Any]:
        """
        Analyzes the LD_PRELOAD environment variable.

        Returns:
            dict[str, Any]: Dictionary with 'active' (bool) and 'message' (str).
        """
        preload = os.environ.get("LD_PRELOAD", "").strip()
        if not preload:
            return {"active": False, "message": "INACTIVE (No preloaded injection vectors)"}

        trusted, external = self._analyze_preload_vectors(preload)
        return {"active": True, "message": self._build_message(trusted, external)}

    def _analyze_preload_vectors(self, preload: str) -> tuple[list[str], list[str]]:
        """
        Categorizes preloaded libraries into trusted and external.

        Args:
            preload: The raw LD_PRELOAD string.

        Returns:
            tuple: (trusted_libs, external_libs)
        """
        # LD_PRELOAD can be space or colon separated
        parts = [p for p in preload.replace(" ", ":").split(":") if p]
        termux_libs = {"libtermux-exec.so", "libtermux.so"}

        trusted = []
        external = []
        for lib in parts:
            if os.path.basename(lib) in termux_libs:
                trusted.append(lib)
            else:
                external.append(lib)
        return trusted, external

    def _build_message(self, trusted: list[str], external: list[str]) -> str:
        """Constructs a descriptive message based on the analysis."""
        if trusted and not external:
            return f"ACTIVE (Trusted Termux Core: {', '.join(trusted)})"
        if trusted and external:
            return (
                f"ACTIVE – Mixed (Trusted: {', '.join(trusted)} | External: {', '.join(external)})"
            )
        return f"ACTIVE – External Hook(s): {', '.join(external)}"


class SUIDBinaryChecker:
    """
    Scans the Termux bin directory for files with SUID or SGID bits.

    Unexpected SUID binaries in the user's bin directory can be a security risk.
    """

    def check(self) -> dict[str, Any]:
        """
        Performs the SUID/SGID scan.

        Returns:
            dict[str, Any]: Dictionary with 'message' (str).
        """
        bin_dir = self._get_bin_dir()
        if not bin_dir:
            return {"message": "PREFIX/bin not found"}

        suid_found = self._scan_bin_dir(bin_dir)
        if suid_found:
            return {"message": f"WARNING – SUID/SGID binaries found: {', '.join(suid_found)}"}
        return {"message": "Pristine (No local SUID anomalies)"}

    def _get_bin_dir(self) -> str | None:
        """Determines the path to the Termux binary directory."""
        prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        bin_dir = os.path.join(prefix, "bin")
        return bin_dir if os.path.isdir(bin_dir) else None

    def _scan_bin_dir(self, bin_dir: str) -> list[str]:
        """Iterates through the bin directory to find SUID/SGID files."""
        suid_found: list[str] = []
        try:
            for entry in os.scandir(bin_dir):
                if entry.is_file(follow_symlinks=False):
                    self._check_file_suid(entry, suid_found)
        except PermissionError:
            pass
        return suid_found

    def _check_file_suid(self, entry: os.DirEntry, suid_found: list[str]):
        """Checks a single file for SUID or SGID bits."""
        try:
            st = entry.stat()
            # stat.S_ISUID is the setuid bit, stat.S_ISGID is the setgid bit
            if st.st_mode & (stat.S_ISUID | stat.S_ISGID):
                suid_found.append(entry.name)
        except (PermissionError, OSError):
            pass


class PermissionChecker:
    """
    Checks for sensitive directory permissions.
    """

    def check(self) -> dict[str, Any]:
        """
        Checks if critical directories have expected permissions.
        """
        prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        home = os.environ.get("HOME", "/data/data/com.termux/files/home")
        return {
            "prefix_writable": os.access(prefix, os.W_OK),
            "home_writable": os.access(home, os.W_OK),
            "prefix": prefix,
        }


class EncryptionChecker:
    """
    Checks the device's encryption status via system properties.
    """

    def check(self) -> dict[str, Any]:
        """
        Retrieves ro.crypto.state and ro.crypto.type.
        """
        results = {"encrypted": False, "state": "unknown", "type": "unknown"}
        try:
            state = self._query_prop("ro.crypto.state")
            crypto_type = self._query_prop("ro.crypto.type")
            results["state"] = state or "unknown"
            results["type"] = crypto_type or "unknown"
            results["encrypted"] = state == "encrypted"
        except Exception:
            pass
        return results

    def _query_prop(self, key: str) -> str | None:
        try:
            res = subprocess.run(["getprop", key], capture_output=True, text=True, check=False)
            return res.stdout.strip() if res.returncode == 0 else None
        except Exception:
            return None


class VulnerabilityChecker:
    """
    Checks for common Android vulnerability indicators like debuggable builds or ADB status.
    """

    def check(self) -> dict[str, Any]:
        """
        Evaluates debuggable status and other risky properties.
        """
        return {
            "debuggable": self._query_prop("ro.debuggable") == "1",
            "secure": self._query_prop("ro.secure") == "1",
            "adb_enabled": self._query_prop("init.svc.adbd") == "running",
        }

    def _query_prop(self, key: str) -> str | None:
        try:
            res = subprocess.run(["getprop", key], capture_output=True, text=True, check=False)
            return res.stdout.strip() if res.returncode == 0 else None
        except Exception:
            return None
