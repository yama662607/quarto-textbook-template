# Changelog

All notable changes to this template will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Added — onboarding for fresh machines

- `scripts/bootstrap.{sh,ps1,py}` — one-shot installer that detects the OS,
  installs `just` / `uv` / `quarto` / `node` via the native package manager
  (brew / apt / dnf / pacman / winget / scoop / curl fallback), then runs
  `uv sync` and `npm install`. Supports `--dry-run` and `--skip-deps`.
- `mise.toml` and `.tool-versions` — version pins for `mise` / `asdf`
  users (`mise install` is enough).
- `.devcontainer/devcontainer.json` — VS Code Dev Containers + GitHub
  Codespaces support; reopens the project with all tools preinstalled and
  forwards port 4312 for `just docs`.
- README "How to use this template" rewritten as a 4-way menu
  (bootstrap script / mise / Codespaces / manual) so users with
  different preferences can pick the path that fits.

## [0.1.0] - 2026-04-26

### Added
- Initial Quarto Book scaffold with KaTeX, Mermaid, sample chapters
- Cross-platform Justfile (Win/Mac/Linux) with standard interface
  (check-env / setup / check / fix / docs)
- Unified `tools/extract_pdf.py` (mode = auto / simple / ocr / latex,
  + `--diagnose`); paired with `tools/render_pdf.py` for image rendering
- Lazy-imported heavy dependencies (`easyocr`, `pix2text`) so base install
  stays slim
- `tools/kill_quarto_process.py` — cross-platform replacement for the
  Unix-only `lsof | xargs kill` idiom
- GitHub Actions: `publish.yml` (gh-pages) + `check.yml`
  (3 OS × Python 3.12 quality matrix, includes Quarto syntax render-check)
- `pyproject.toml` with PEP 735 `dependency-groups` and feature extras
  (ocr / math / notebook / quantum / shiny / viz / debug)
- AI agent integration:  `AGENTS.md` (agents.md spec compliant),
  `CLAUDE.md` and `GEMINI.md` thin wrappers that `@AGENTS.md`
- MIT LICENSE, CODEOWNERS, SECURITY.md, CHANGELOG.md
