#!/usr/bin/env python3
"""Bootstrap the development environment from a fresh machine.

Installs (if missing): just, uv, quarto, node, then runs `uv sync` and
`npm install`. After this finishes, `just docs` should work.

Usage:
  python3 scripts/bootstrap.py              # detect OS, install everything
  python3 scripts/bootstrap.py --dry-run    # print what would happen
  python3 scripts/bootstrap.py --skip-deps  # only install tools, skip uv sync / npm install

This file is the shared implementation. The thin OS-specific entry points
(`scripts/bootstrap.sh`, `scripts/bootstrap.ps1`) just locate Python and
re-exec this script.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Tool catalogue
# ---------------------------------------------------------------------------
# `cmd` is the executable name we probe for via `shutil.which`.
TOOLS = ["just", "uv", "quarto", "node"]


def _is_installed(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(cmd: list[str] | str, *, dry: bool, shell: bool = False) -> int:
    pretty = cmd if isinstance(cmd, str) else " ".join(cmd)
    print(f"  $ {pretty}")
    if dry:
        return 0
    return subprocess.call(cmd, shell=shell)


# ---------------------------------------------------------------------------
# Per-OS install strategies
# ---------------------------------------------------------------------------


def install_macos(missing: list[str], dry: bool) -> None:
    if not _is_installed("brew"):
        print(
            "Homebrew is not installed. Install it first:\n"
            '  /bin/bash -c "$(curl -fsSL '
            'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        )
        sys.exit(1)
    formula_map = {
        "just": ["brew", "install", "just"],
        "uv": ["brew", "install", "uv"],
        "quarto": ["brew", "install", "--cask", "quarto"],
        "node": ["brew", "install", "node"],
    }
    for tool in missing:
        _run(formula_map[tool], dry=dry)


def install_linux(missing: list[str], dry: bool) -> None:
    """Try apt → dnf → pacman, then fall back to upstream curl installers."""
    apt = _is_installed("apt-get")
    dnf = _is_installed("dnf")
    pac = _is_installed("pacman")

    for tool in missing:
        if tool == "uv":
            _run("curl -LsSf https://astral.sh/uv/install.sh | sh", dry=dry, shell=True)
        elif tool == "node":
            if apt:
                _run(
                    "sudo apt-get update && sudo apt-get install -y nodejs npm", dry=dry, shell=True
                )
            elif dnf:
                _run(["sudo", "dnf", "install", "-y", "nodejs", "npm"], dry=dry)
            elif pac:
                _run(["sudo", "pacman", "-S", "--noconfirm", "nodejs", "npm"], dry=dry)
            else:
                print("  no supported package manager — install node 20+ from https://nodejs.org/")
        elif tool == "just":
            if pac:
                _run(["sudo", "pacman", "-S", "--noconfirm", "just"], dry=dry)
            else:
                # Official prebuilt-binary installer (works on any glibc Linux).
                _run(
                    "curl --proto '=https' --tlsv1.2 -sSf "
                    "https://just.systems/install.sh | bash -s -- --to ~/.local/bin",
                    dry=dry,
                    shell=True,
                )
                print("  reminder: ensure ~/.local/bin is on $PATH")
        elif tool == "quarto":
            print("  Quarto: install the .deb / .rpm from https://quarto.org/docs/get-started/")


def install_windows(missing: list[str], dry: bool) -> None:
    """Prefer winget → scoop. Print fallback URLs when neither works."""
    have_winget = _is_installed("winget")
    have_scoop = _is_installed("scoop")

    winget_ids = {
        "just": "Casey.Just",
        "uv": "astral-sh.uv",
        "quarto": "Posit.Quarto",
        "node": "OpenJS.NodeJS.LTS",
    }
    scoop_pkgs = {
        "just": "just",
        "uv": "uv",
        "quarto": "quarto",
        "node": "nodejs-lts",
    }
    for tool in missing:
        if have_winget:
            _run(["winget", "install", "--id", winget_ids[tool], "-e", "--silent"], dry=dry)
        elif have_scoop:
            _run(["scoop", "install", scoop_pkgs[tool]], dry=dry)
        else:
            print(
                f"  Neither winget nor scoop found. Install {tool} manually:\n"
                f"    just  → https://github.com/casey/just/releases\n"
                f"    uv    → https://docs.astral.sh/uv/getting-started/installation/\n"
                f"    quarto→ https://quarto.org/docs/get-started/\n"
                f"    node  → https://nodejs.org/"
            )
            return


# ---------------------------------------------------------------------------
# Project deps
# ---------------------------------------------------------------------------


def install_project_deps(dry: bool) -> None:
    print("\n--- Project dependencies ---")
    if _is_installed("uv"):
        _run(["uv", "sync"], dry=dry)
    else:
        print("  skip uv sync (uv not on PATH yet — re-run after restarting your shell)")
    if _is_installed("npm"):
        _run(["npm", "install"], dry=dry)
    else:
        print("  skip npm install (node not on PATH yet — re-run after restarting your shell)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description="Bootstrap the dev environment.")
    p.add_argument("--dry-run", action="store_true", help="Print commands without executing.")
    p.add_argument(
        "--skip-deps",
        action="store_true",
        help="Install tools only; skip `uv sync` and `npm install`.",
    )
    args = p.parse_args()

    print(f"Project root: {ROOT}")
    print(f"Platform    : {sys.platform}")

    missing = [t for t in TOOLS if not _is_installed(t)]
    if missing:
        print(f"Missing     : {', '.join(missing)}")
    else:
        print("All required tools already installed.")

    if missing:
        print("\n--- Installing missing tools ---")
        if sys.platform == "darwin":
            install_macos(missing, args.dry_run)
        elif sys.platform.startswith("linux"):
            install_linux(missing, args.dry_run)
        elif sys.platform == "win32":
            install_windows(missing, args.dry_run)
        else:
            print(f"Unsupported platform: {sys.platform}")
            return 1

    if not args.skip_deps:
        install_project_deps(args.dry_run)

    print(
        "\nDone. If commands were just installed, restart your shell so PATH picks them "
        "up, then run:\n  just check-env\n  just docs"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
