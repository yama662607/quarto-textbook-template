"""Report Quarto version-sensitive capabilities for this template."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "utils"))

from find_quarto import find_quarto  # noqa: E402


@dataclass(frozen=True)
class Capability:
    name: str
    since: tuple[int, int]
    template_status: str
    note: str


CAPABILITIES = [
    Capability(
        "axe HTML accessibility checks",
        (1, 8),
        "opt-in profile",
        "Use `just render-a11y` or `just docs-a11y` for local checks.",
    ),
    Capability(
        "list tables",
        (1, 9),
        "showcase adopted",
        "Used in `quarto/textbook/_07_figures_and_tables.qmd`.",
    ),
    Capability(
        "PDF standards (`pdf-standard`)",
        (1, 9),
        "documented opt-in",
        "Requires PDF/A or PDF/UA intent and optional veraPDF validation.",
    ),
    Capability(
        "LLM-friendly website output (`llms-txt`)",
        (1, 9),
        "documented opt-in",
        "Official docs currently describe this for website config; verify before enabling on books.",
    ),
    Capability(
        "`quarto use brand`",
        (1, 9),
        "documented opt-in",
        "Useful when multiple textbooks should share external brand assets.",
    ),
    Capability(
        "Typst book output",
        (1, 9),
        "documented opt-in",
        "Keep separate from the default XeLaTeX PDF path.",
    ),
]


def parse_version(text: str) -> tuple[int, int, int] | None:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", text)
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def version_at_least(version: tuple[int, int, int], minimum: tuple[int, int]) -> bool:
    return (version[0], version[1]) >= minimum


def main() -> int:
    quarto = find_quarto()
    if not quarto:
        print("Quarto not found. Install Quarto first.")
        return 1

    try:
        raw_version = subprocess.check_output(
            [quarto, "--version"], stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as exc:
        print(f"Failed to run `{quarto} --version`: {exc.output}")
        return 1

    version = parse_version(raw_version)
    print(f"Quarto: {raw_version.strip()} ({quarto})")
    if version is None:
        print("Could not parse Quarto version; capability status is unknown.")
        return 1

    print("\nTemplate capability matrix:")
    for capability in CAPABILITIES:
        status = (
            "available" if version_at_least(version, capability.since) else "needs newer Quarto"
        )
        since = f"{capability.since[0]}.{capability.since[1]}+"
        print(f"- {capability.name} [{since}]: {status}")
        print(f"  template: {capability.template_status}")
        print(f"  note: {capability.note}")

    print("\nReferences:")
    print("- docs/quarto-modern.md")
    print("- https://quarto.org/docs/download/release.html")
    print("- https://quarto.org/docs/output-formats/html-accessibility.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
