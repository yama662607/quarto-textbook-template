"""Run a Quarto command while holding the project render lock."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from utils.quarto_lock import QuartoLock, QuartoLockError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a command while preventing concurrent Quarto render/preview."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Seconds to wait for the lock. Default: fail immediately.",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after --")
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("missing command")

    project_root = Path(__file__).parent.parent.resolve()
    try:
        with QuartoLock(project_root, timeout=args.timeout):
            return subprocess.call(command, cwd=project_root)
    except QuartoLockError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
