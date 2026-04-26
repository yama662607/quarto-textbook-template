# Changelog

All notable changes to this template will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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
