import os
import stat
import subprocess
from typing import Any, Protocol


class SecurityChecker(Protocol):
    def check(self) -> dict[str, Any]:
        """Performs a security check and returns result data."""
        ...


class RootPresenceChecker:
    def check(self) -> dict[str, Any]:
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
        found_nonsetuid = []
        errors = []
        for path in su_paths:
            found_setuid = self._check_single_su_path(path, found_nonsetuid, errors)
            if found_setuid:
                return [], [], found_setuid
        return found_nonsetuid, errors, None

    def _check_single_su_path(
        self, path: str, found_nonsetuid: list[str], errors: list[str]
    ) -> str | None:
        try:
            st = os.stat(path)
            if not stat.S_ISREG(st.st_mode):
                return None
            if st.st_mode & stat.S_ISUID:
                return path
            found_nonsetuid.append(path)
        except (FileNotFoundError, PermissionError):
            pass
        except Exception as e:
            errors.append(f"{path} ({e})")
        return None

    def _format_root_result(self, found_nonsetuid: list[str], errors: list[str]) -> dict[str, Any]:
        if found_nonsetuid:
            return {
                "found": False,
                "message": f"Found but NO setuid bit: {', '.join(found_nonsetuid)}",
            }
        if errors:
            return {"found": False, "message": f"Could not read all paths: {'; '.join(errors)}"}
        return {"found": False, "message": "PRISTINE (No su binary found)"}


class SELinuxStatusChecker:
    def check(self) -> dict[str, Any]:
        return {"status": self._get_status()}

    def _get_status(self) -> str:
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
        try:
            with open("/sys/fs/selinux/enforce", "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val == "1":
                    return "Enforcing (Strict Sandbox active)"
                if val == "0":
                    return "Permissive (SELinux is loaded but not enforcing)"
        except (FileNotFoundError, PermissionError):
            pass
        return None

    def _check_getenforce_cmd(self) -> str | None:
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
    def check(self) -> dict[str, Any]:
        preload = os.environ.get("LD_PRELOAD", "").strip()
        if not preload:
            return {"active": False, "message": "INACTIVE (No preloaded injection vectors)"}

        trusted, external = self._analyze_preload_vectors(preload)
        return {"active": True, "message": self._build_message(trusted, external)}

    def _analyze_preload_vectors(self, preload: str) -> tuple[list[str], list[str]]:
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
        if trusted and not external:
            return f"ACTIVE (Trusted Termux Core: {', '.join(trusted)})"
        if trusted and external:
            return (
                f"ACTIVE – Mixed (Trusted: {', '.join(trusted)} | External: {', '.join(external)})"
            )
        return f"ACTIVE – External Hook(s): {', '.join(external)}"


class SUIDBinaryChecker:
    def check(self) -> dict[str, Any]:
        bin_dir = self._get_bin_dir()
        if not bin_dir:
            return {"message": "PREFIX/bin not found"}

        suid_found = self._scan_bin_dir(bin_dir)
        if suid_found:
            return {"message": f"WARNING – SUID/SGID binaries found: {', '.join(suid_found)}"}
        return {"message": "Pristine (No local SUID anomalies)"}

    def _get_bin_dir(self) -> str | None:
        prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        bin_dir = os.path.join(prefix, "bin")
        return bin_dir if os.path.isdir(bin_dir) else None

    def _scan_bin_dir(self, bin_dir: str) -> list[str]:
        suid_found = []
        try:
            for entry in os.scandir(bin_dir):
                if entry.is_file(follow_symlinks=False):
                    self._check_file_suid(entry, suid_found)
        except PermissionError:
            pass
        return suid_found

    def _check_file_suid(self, entry: os.DirEntry, suid_found: list[str]):
        try:
            st = entry.stat()
            if st.st_mode & (stat.S_ISUID | stat.S_ISGID):
                suid_found.append(entry.name)
        except (PermissionError, OSError):
            pass
