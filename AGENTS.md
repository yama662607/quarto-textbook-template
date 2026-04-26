# AGENTS.md

> AI コーディングエージェント (Claude Code, Codex, Cursor, Copilot, Gemini CLI 等) 向けの規約。
> 本ファイルは [agents.md](https://agents.md) 仕様に準拠します。Claude Code は `CLAUDE.md`、Gemini CLI は `GEMINI.md` から本ファイルを参照します。

## Project overview

Quarto Book ベースの教科書 / 講義ノートサイト。HTML を GitHub Pages、PDF をオプションで生成。本文は `quarto/textbook/textbook.qmd` を信頼できる唯一の情報源 (single source of truth) とし、章ごとのコンテンツは `_*.qmd` パーシャルに分割して `{{< include >}}` で統合する。

## Setup commands

```bash
just check-env   # ツール (uv / just / quarto / npm) 確認
just setup       # uv sync + npm install
just docs        # http://localhost:4312 でプレビュー
```

## ⚠️ PDF 取り込みの必須ワークフロー

qmd を書き起こす前に、**`render-pdf` と `extract-pdf` の両方を必ず実行** し、画像と文字情報を**照合**してください。

```bash
# 1. ページ画像化 (視覚情報)
just render-pdf <pdf_path> <start_page> <end_page>
# → /tmp/page_NN.png

# 2. 文字情報抽出 (text / OCR / LaTeX 数式) — どのモードを使うか分からなければ先に診断
just diagnose-pdf <pdf_path>
just extract-pdf <pdf_path> --start <start> --end <end>     # mode=auto がデフォルト
# 必要に応じて --mode {simple, ocr, latex} を明示
```

**どちらか一方では不十分:**
- 抽出のみ → OCR 誤読、数式記号の取りこぼし、図表構造の見落としが発生
- 画像のみ → 数式の LaTeX 化や引用テキスト書き起こしが手作業で時間浪費

抽出結果は **必ず元画像と突き合わせて誤読をチェック** してから qmd に書き起こすこと。

## Code style

- **Quarto/qmd**:
  - 本文は `_*.qmd` (アンダースコア接頭辞 = レンダリング対象から除外) に分割し、`textbook.qmd` から `{{< include >}}`
  - パーシャルファイルに **YAML フロントマターを書かない** (親ファイルに集約)
  - `:::` (fenced div) の **閉じる前に空行必須** (`just fix` で自動修正可)
  - 数式: インライン `$...$`、ディスプレイ `$$...$$ {#eq-label}`、参照は `@eq-label`
  - 図表: Mermaid (`{mermaid}` ブロック)、PNG/JPG は `quarto/assets/images/`
- **Python** (`tools/` 配下): ruff format / lint, mypy, line-length 100
- **PDF リンク** (見出し横): `## タイトル [p.12](../assets/pdf/textbook.pdf#page=12) {#sec-anchor}`
  - ページ番号と物理ページのオフセットは PDF ごとに `just diagnose-pdf` で確認

## Testing

```bash
just check       # 品質ゲート (fmt + lint + typecheck + validate-docs + render-check + pytest)
just fix         # 自動修正 (fmt + lint + validate-docs --fix)
just validate-docs   # ドキュメント整合性検証 (Quarto / Mermaid / LaTeX)
just test        # pytest のみ
```

ドキュメント編集後は **必ず `just check` を実行**。エラーがあれば `just fix` → `just check` の順で。

## Commit & PR

- ブランチ: `feature/<topic>` または `fix/<topic>`
- コミットメッセージ: 日本語可、変更の **why** を 1 行目に
- PR は `main` 向けに、CI (3 OS × Python 3.12 + Quarto render-check) がグリーンになるまで merge しない

## Security & forbidden actions

- ❌ `pip install` を提案しない → `uv add <pkg>` または `uv sync --extra <name>` を使う
- ❌ `_*.qmd` に YAML ヘッダーを追加しない
- ❌ `quarto/textbook/chapter1.qmd` のような新規ルート qmd を作らない (パーシャルに分ける)
- ❌ `:::` の閉じる前の空行を省略しない
- ❌ Justfile に Unix 専用コマンド (`lsof`, `pkill`, `xargs`, `export PATH=`) を追加しない → 必ず `tools/*.py` 経由で cross-platform 化
- ❌ `quarto/assets/raw/`, `quarto/assets/private/`, `research/inbox/*/` 配下のファイルを commit しない (gitignore 済)

## Deployment

`main` ブランチへの push で `.github/workflows/publish.yml` が走り、`gh-pages` ブランチに自動デプロイ → GitHub Pages で公開。

教科書本文で optional 機能 (Qiskit / Shinylive / Jupyter compute / OCR / LaTeX) を使う場合は `publish.yml` の `uv sync` 行に `--extra <name>` を追記すること (デフォルトは base のみで軽量化)。

## Tooling reference (Justfile)

| コマンド | 用途 |
| --- | --- |
| `just check-env` | ツール存在確認 |
| `just setup` | 依存インストール |
| `just check` | 品質ゲート (CI と同等) |
| `just fix` | 自動修正 |
| `just docs` | プレビューサーバー起動 |
| `just fix-docs` | プレビュー復旧 (Win/Mac/Linux 対応) |
| `just validate-docs` | ドキュメント検証 |
| `just render-site` | HTML 実レンダリング |
| `just render-book-pdf` | PDF 実レンダリング |
| `just diagnose-pdf <pdf>` | PDF 構造診断 |
| `just render-pdf <pdf> <s> <e>` | PDF ページ画像化 |
| `just extract-pdf <pdf> [opts]` | 文字・数式抽出 (mode=auto/simple/ocr/latex) |
