# AI エージェント向けガイド

このリポジトリで AI エージェント (Claude Code, Codex, Gemini CLI 等) が作業する際の規約をまとめます。**ドキュメント整合性を保つため、以下のルールに従ってください。**

## 1. プロジェクト構造の原則

### 1.1 信頼できる唯一の情報源 (Single Source of Truth)
- **メイン教科書**: `quarto/textbook/textbook.qmd`
- すべての本文は `textbook.qmd` に `{{< include _NN_*.qmd >}}` 形式で統合
- 章ごとの新規 `*.qmd` をルートに作らない (例: `quarto/textbook/chapter1.qmd` は禁止)

### 1.2 パーシャル (断片) ファイル `_*.qmd`
- **場所**: `quarto/textbook/` 直下、または章フォルダ
- **命名**: 必ずアンダースコアで始める (Quarto がレンダリング対象から除外)
- **内容**: 純粋な Markdown / Quarto コンテンツのみ。**YAML フロントマター禁止**
- **インクルード**: `textbook.qmd` 側で `{{< include _01_introduction.qmd >}}`

### 1.3 PDF リンク戦略
原 PDF を `quarto/assets/pdf/` に置いた場合、見出し横にリンクを付与:

```markdown
## 第1.2節 タイトル [p.12](../assets/pdf/textbook.pdf#page=12) {#sec-anchor}
```

ページ番号と物理ページのオフセットは PDF ごとに異なるので、最初に `just diagnose-pdf <pdf>` で確認すること。

### 1.4 テンプレート
- **場所**: `quarto/templates/`
- **執筆用**: `textbook_template.qmd` (新規章作成時にコピー)
- **部品集**: `quarto_feature_showcase.qmd` (callout / Mermaid / 数式の書き方リファレンス)

## 2. 品質基準

1. **完全な数式記述** — 文章だけで説明せず、必ず厳密な LaTeX 数式を併記
2. **物理学的・直感的な解説** — 数学定義に加えて直感的な対応関係を補足
3. **視覚的補助** — 概念関係図は Mermaid (`flowchart`, `sequenceDiagram` 等) で
4. **PDF リンク配置** — `##` / `###` 見出しに対応 PDF ページリンクを付与
5. **Fenced Div の書式** — `:::` の **閉じる前に空行必須** (Quarto/Pandoc パース失敗回避)。`just fix` で自動修正可

## 3. ワークフロー

### 3.1 PDF 取り込み

```bash
# Step 0: PDF 構造診断 (テキスト埋込有無を確認)
just diagnose-pdf quarto/assets/pdf/textbook.pdf

# Step 1: ページ画像化 (視覚情報の確定)
just render-pdf quarto/assets/pdf/textbook.pdf 30 32

# Step 2A: テキスト埋込済の場合
just extract-pdf quarto/assets/pdf/textbook.pdf

# Step 2B: 画像 PDF (スキャン / 古い教科書) の場合
uv sync --extra ocr
just extract-pdf-ocr quarto/assets/pdf/textbook.pdf

# Step 2C: 数式まで LaTeX で抽出したい場合
uv sync --extra math
just extract-content quarto/assets/pdf/textbook.pdf 30 32
```

**重要**: OCR / 数式抽出の結果は**必ず元画像と照合**して誤読をチェックすること。

### 3.2 編集後の検証

コード/ドキュメントを変更したら **必ず** 実行:

```bash
just fix      # 自動修正 (fmt + lint + validate-docs --fix)
just check    # 品質ゲート
```

### 3.3 デプロイ

`main` ブランチへ push すると `.github/workflows/publish.yml` が走り、`gh-pages` ブランチに自動公開されます。手動デプロイは不要。

## 4. Justfile タスク一覧

| コマンド | 用途 |
| --- | --- |
| `just check-env` | 必要ツール (uv/just/quarto/npm) の確認 |
| `just setup` | 依存インストール |
| `just check` | 品質ゲート (CI と同等) |
| `just fix` | 自動修正 |
| `just docs` | プレビューサーバー起動 |
| `just fix-docs` | プレビュー復旧 (Win/Mac/Linux 対応) |
| `just validate-docs` | ドキュメント検証 |
| `just render-site` | HTML 実レンダリング |
| `just diagnose-pdf <pdf>` | PDF 構造診断 |
| `just render-pdf <pdf> <s> <e>` | PDF ページ画像化 |
| `just extract-pdf <pdf>` | テキスト抽出 (埋込済) |
| `just extract-pdf-ocr <pdf>` | OCR 抽出 (画像 PDF) |
| `just extract-content <pdf> <s> <e>` | テキスト+数式 (LaTeX) 抽出 |

## 5. 禁止事項

- ❌ `pip install` を提案 → `uv add <pkg>` または `uv sync --extra <group>` を使う
- ❌ `_*.qmd` に YAML ヘッダーを追加
- ❌ `quarto/textbook/chapter1.qmd` のような新規ルート qmd 作成
- ❌ `:::` の閉じる前の空行を省略
- ❌ Unix 専用コマンド (`lsof`, `pkill`, `xargs`, `export`) を Justfile に追加 → 必ず Python 化

## 6. 初回オンボーディング

新しく参加するエージェントは:

```bash
just check-env       # ツール確認
just setup           # 依存同期
just validate-docs   # 既存ドキュメントの整合性確認
just docs            # プレビューを開いて全体把握
```
