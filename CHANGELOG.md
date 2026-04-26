# Changelog

All notable changes to this template will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Quarto Live (Pyodide) integration

- Bundled `r-wasm/quarto-live` extension under `quarto/_extensions/r-wasm/live/`
- Bundled `Noto Sans JP` (SIL OFL 1.1) under `quarto/assets/fonts/` so
  matplotlib in Pyodide can render Japanese titles / labels without "tofu"
- Added a working sample chapter `_03_interactive_demo.qmd` that demonstrates:
  - `{ojs}` slider with LaTeX labels (`tex` template literal)
  - `{pyodide}` cell with `#| autorun: true` + `#| input:` for reactive
    re-execution on slider change
  - Inline font-load idiom (`pyfetch` + `font_manager.fontManager.addfont`)
    placed at the top of the drawing cell so font registration happens
    before the first draw — splitting it into a separate setup cell does
    NOT preserve order under Quarto Live and produces a flood of
    `Glyph missing from current font` warnings
- `_quarto.yml` `project.resources` now includes `assets/fonts/**/*` so
  the font is published with the site
- AGENTS.md gained a "対話シミュレーション" section documenting the
  pattern, the forbidden alternatives (separate font cell, `pyodide.resources`
  in qmd YAML — neither works under filter mode), and the per-page recipe

### Hardening pass (review feedback from 4 sub-agents)

- `scripts/bootstrap.py`: failures are now collected and reported in a
  final summary; the script returns a non-zero exit code on partial
  failure (was always 0 → silent fail). Added Alpine (`apk`) and
  openSUSE (`zypper`) package managers. Quarto on Linux now produces a
  clear "manual install required" message with the official URL.
- `Justfile setup`: dropped `--all-extras` (was contradicting README's
  "lightweight base" promise and silently downloading 1 GB+). Added
  `setup-all` for the explicit opt-in.
- `mise.toml`: clarified that mise does NOT manage Quarto, with explicit
  install commands per OS.
- `tools/render_pdf.py`: replaced `default="/tmp"` with
  `tempfile.gettempdir()` (was breaking on Windows). Added page range
  validation, accepted both `--out-dir` and `--out_dir`.
- `tools/extract_pdf.py`: page range validation (start>end, etc.),
  `with fitz.open(...)` to release docs on exception, UTF-8 stdout
  reconfigure for Windows cp932, ValueError caught at main() for clean
  user-facing errors.
- `tools/utils/quarto_watcher.py`: replaced "append space + truncate"
  (race-prone, cp932-fragile) with `Path.touch()`.
- `tools/utils/latex_extraction.py` / `tools/clean.py`: dropped bare
  `except` swallowing.
- `tools/kill_quarto_process.py`: two-tier strategy — try cheap
  system-wide `net_connections()` first, fall back to per-process
  iteration only when denied (faster on most systems).
- `.github/workflows/publish.yml`: switched curl-pipe-bash uv install
  to `astral-sh/setup-uv@v3` (matches check.yml).
- `.github/workflows/check.yml`: added `persist-credentials: false` on
  `actions/checkout` (read-only job, no need for token reuse).
- `.github/dependabot.yml`: weekly bumps for GitHub Actions / pip / npm
  / devcontainers — sets the stage for tag→SHA pin migration.
- `SECURITY.md`: expanded hardening guide (Dependabot, npm/uv audit,
  optional-feature warnings, migration to `actions/deploy-pages`).
- Docs: AGENTS.md tooling reference now lists every Justfile recipe and
  matches extras names with `pyproject.toml`. README placeholder list
  adds `CODEOWNERS`, `.devcontainer name`, `SECURITY.md`,
  `quarto/textbook/textbook.qmd`. `gh` CLI is no longer the only path
  shown — Web UI flow first.
- `tools/README.md`: added an ASCII decision tree for picking the right
  `extract_pdf --mode`.
- `CLAUDE.md` / `GEMINI.md`: added a header explaining that the file
  is intentionally short and the `@AGENTS.md` line is the import syntax
  (so future readers do not mistake them for broken stubs).
- `.devcontainer/devcontainer.json`: added inline notes about the
  third-party uv feature and 5–10 minute initial build time.

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
