# =============================================================================
# Quarto Textbook Template — Justfile
# =============================================================================
# Cross-platform (Windows / macOS / Linux). All shell-out work is delegated to
# Python helpers under tools/ so PowerShell and POSIX shells behave identically.
# =============================================================================

set dotenv-load := true
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

pm := "uv"
python := "uv run python"

# デフォルト: 全体の品質チェックを実行
default: check

# =============================================================================
# Standard Interface (AI Agent Protocol)
# =============================================================================

# 環境の整合性チェック (uv / just / quarto / npm)
check-env:
    @{{python}} tools/check_env.py

# 環境構築: 依存関係のインストール
setup: check-env
    @echo "Setting up environment..."
    {{pm}} sync --all-extras
    npm install
    @echo "Environment setup complete."

# 全体品質検証 (CI ゲート)
check: fmt-check lint typecheck validate-docs test
    @echo "All quality checks passed."

# フル品質検証: HTML 実レンダリングまで含めて確認
check-full: check render-site
    @echo "Full quality checks passed."

# 自動修正
fix: fmt lint-fix validate-docs-fix
    @echo "Auto-fixes applied."

# =============================================================================
# Testing & Verification
# =============================================================================

test *args="":
    @echo "Running unit tests..."
    {{pm}} run pytest {{args}}

# =============================================================================
# Granular Tasks
# =============================================================================

fmt-check:
    {{pm}} run ruff format --check

fmt:
    {{pm}} run ruff format

lint:
    {{pm}} run ruff check

lint-fix:
    {{pm}} run ruff check --fix

typecheck:
    {{pm}} run mypy tools

# =============================================================================
# Operations & Utilities
# =============================================================================

# ビルド成果物・キャッシュ削除 (Cross-platform)
clean:
    {{python}} tools/clean.py

# =============================================================================
# Quarto Tasks
# =============================================================================

# Quarto プレビュー起動 (port 4312)
docs:
    @{{python}} tools/dev_server.py

# プレビューが落ちない / ポートが使用中の場合の復旧 (Win/Mac/Linux 対応)
fix-docs:
    @echo "Killing lingering Quarto processes on port 4312..."
    @{{python}} tools/kill_quarto_process.py --port 4312

# Quarto HTML 実レンダリング
render-site:
    quarto render quarto --to html

# Quarto PDF 実レンダリング
render-book-pdf:
    quarto render quarto --to pdf

# ドキュメント整合性検証 (Quarto / Mermaid / LaTeX)
validate-docs:
    {{python}} tools/validate_docs.py quarto/

validate-docs-no-cache:
    {{python}} tools/validate_docs.py quarto/ --no-cache

validate-docs-fix:
    {{python}} tools/validate_docs.py quarto/ --fix

clear-validation-cache:
    {{python}} tools/validate_docs.py --clear-cache

# =============================================================================
# PDF Ingestion (choose the variant that matches your source)
# =============================================================================

# テキスト埋込済 PDF からテキスト+画像抽出 (簡易・依存少)
extract-pdf pdf_path *args="":
    {{python}} tools/extract_pdf_simple.py {{pdf_path}} {{args}}

# 画像 PDF (テキスト未埋込・スキャン PDF) を OCR で読み取る (easyocr)
extract-pdf-ocr pdf_path *args="":
    {{python}} tools/extract_pdf_ocr.py {{pdf_path}} {{args}}

# PDF からテキスト+数式(LaTeX) 抽出 (pix2text、要 GPU 推奨)
# 使い方: just extract-content <pdf_path> <start_page> <end_page>
extract-content pdf_path start end *args="":
    {{python}} tools/extract_pdf_content.py {{pdf_path}} --start {{start}} --end {{end}} {{args}}

# 教科書 PDF の画像化 (PNG 出力)
# 使い方: just render-pdf <pdf_path> <start_page> <end_page>
render-pdf pdf_path start end *args="":
    {{python}} tools/render_pdf.py {{pdf_path}} --start {{start}} --end {{end}} {{args}}

# PDF 構造診断 (テキスト埋込有無、ページ数等)
diagnose-pdf pdf_path:
    {{python}} tools/diagnose_pdf.py {{pdf_path}}

# =============================================================================
# Optional: Streamlit / Shiny app launcher
# =============================================================================

# Streamlit アプリ起動: just app <path>
app path:
    {{python}} -m streamlit run {{path}}
