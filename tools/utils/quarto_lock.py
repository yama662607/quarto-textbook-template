"""Cross-platform lock for Quarto render/preview commands."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path


class QuartoLockError(RuntimeError):
    """Raised when another Quarto command already owns the lock."""


class QuartoLock:
    """A small lock-file guard for Quarto commands that share `_book`.

    The lock is intentionally non-reentrant across processes. It prevents
    accidental concurrent `quarto render` / `quarto preview` runs, which can
    race while moving `_book` files.
    """

    def __init__(self, project_root: Path, *, timeout: float = 0.0) -> None:
        self.project_root = project_root
        self.timeout = timeout
        self.path = project_root / ".quarto-render.lock"
        self._fd: int | None = None

    def __enter__(self) -> QuartoLock:
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                message = f"pid={os.getpid()}\nstarted={time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n"
                os.write(self._fd, message.encode("utf-8"))
                return self
            except FileExistsError as exc:
                if self._remove_stale_lock():
                    continue
                if self.timeout <= 0 or time.monotonic() >= deadline:
                    owner = self._read_owner()
                    detail = f" Existing lock: {owner}" if owner else ""
                    raise QuartoLockError(
                        "Another Quarto render/preview command is running."
                        f"{detail}\n"
                        "Stop the other command or run `just fix-docs` if the preview server is stale."
                    ) from exc
                time.sleep(0.25)

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass

    def _read_owner(self) -> str:
        try:
            return self.path.read_text(encoding="utf-8").strip().replace("\n", "; ")
        except OSError:
            return ""

    def _remove_stale_lock(self) -> bool:
        owner = self._read_owner()
        match = re.search(r"pid=(\d+)", owner)
        if not match:
            return False
        pid = int(match.group(1))
        if self._pid_exists(pid):
            return False
        try:
            self.path.unlink()
            return True
        except FileNotFoundError:
            return True
        except OSError:
            return False

    @staticmethod
    def _pid_exists(pid: int) -> bool:
        try:
            import psutil  # type: ignore

            return psutil.pid_exists(pid)
        except ImportError:
            pass
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return True
        return True
