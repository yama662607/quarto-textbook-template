# Quarto Textbook Template

教科書・授業ノート・写真や PDF など各種素材から **Quarto** ドキュメントを構築し、**GitHub Pages** に公開するためのテンプレートリポジトリです。

> [!TIP]
> このリポジトリは GitHub の "**Use this template**" ボタンから新規プロジェクトとして即コピーできます。

## 主な特徴

- **Quarto Book** ベース (HTML / PDF 両対応)
- **PDF 取り込みツール群** — テキスト埋込済 / 画像 PDF (OCR) / 数式 (LaTeX) のすべてに対応
- **Mermaid / KaTeX** によるダイアグラム & 数式
- **Justfile** による統一コマンドインターフェース (Win/Mac/Linux)
- **GitHub Actions** で push 時に自動公開
- **品質ゲート**: ruff + mypy + pytest + Quarto/Mermaid/LaTeX 整合性検証
- **AI エージェント対応** (`AGENTS.md` 同梱)

## クイックスタート

### 1. テンプレートからリポジトリ作成

GitHub の "Use this template" → "Create a new repository" でクローン。または:

```bash
gh repo create my-textbook --template yama662607/quarto-textbook-template --public --clone
cd my-textbook
```

### 2. 必要ツールのインストール

| ツール | macOS | Linux | Windows |
| --- | --- | --- | --- |
| **Python 3.12+** | `brew install python@3.12` | apt/dnf | [python.org](https://www.python.org/) |
| **uv** | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **just** | `brew install just` | `cargo install just` または [snap/apt](https://github.com/casey/just#packages) | `winget install Casey.Just` または `scoop install just` |
| **Quarto** | `brew install --cask quarto` | [.deb / .rpm](https://quarto.org/docs/get-started/) | [installer](https://quarto.org/docs/get-started/) |
| **Node.js 20+** | `brew install node` | nvm/apt | [nodejs.org](https://nodejs.org/) |

### 3. セットアップ & プレビュー

```bash
just setup    # uv sync + npm install
just docs     # http://localhost:4312 でライブプレビュー
```

### 4. プロジェクト名などの書き換え

以下のファイル中のプレースホルダを置換してください:

- `pyproject.toml`: `name`, `description`, `authors`
- `package.json`: `name`, `description`
- `quarto/_quarto.yml`: `book.title`, `book.author`, `page-footer`
- `quarto/index.qmd`: タイトルと本文
- `LICENSE`: copyright 年と保有者
- `README.md`: このファイル全体

### 5. GitHub Pages の有効化

1. GitHub リポジトリの Settings → Pages → Source を **`gh-pages` branch** に設定
2. `git push origin main` すると `.github/workflows/publish.yml` が走り、自動で公開されます

## ディレクトリ構成

```
.
├── quarto/                  # Quarto ソース
│   ├── _quarto.yml         # サイト設定
│   ├── index.qmd           # トップページ
│   ├── textbook/           # 本編 (textbook.qmd + _*.qmd で章分割)
│   ├── templates/          # CSS / sidebar JS / qmd テンプレ
│   ├── preamble.tex        # PDF 出力用 LaTeX プリアンブル
│   └── assets/             # 画像・PDF など
│       ├── images/         # 公開図版
│       ├── pdf/            # 公開 PDF
│       ├── raw/            # 個人保管 (gitignore)
│       └── private/        # 機密素材 (gitignore)
├── research/               # 素材インテイク・下書き
│   ├── inbox/             # 取り込み待ち素材
│   ├── notes/             # 個人メモ
│   ├── drafts/            # 公開前下書き
│   └── guidelines/        # 編集ガイドライン
├── tools/                  # 開発支援スクリプト (Python)
│   ├── README.md          # 各ツールの用途と出自
│   ├── check_env.py       # 環境チェック
│   ├── dev_server.py      # Quarto preview + watcher
│   ├── validate_docs.py   # Quarto/Mermaid/LaTeX 検証
│   ├── extract_pdf_*.py   # PDF 抽出 (3種)
│   ├── render_pdf*.py     # PDF 画像化
│   ├── diagnose_pdf.py    # PDF 構造診断
│   └── kill_quarto_process.py # Win 対応プロセス停止
├── tests/                  # pytest
├── .github/workflows/      # CI/CD
├── Justfile                # 統一コマンド
├── pyproject.toml          # Python 依存
├── package.json            # Node 依存
├── AGENTS.md               # AI エージェント向け指示
└── LICENSE                 # MIT
```

## コマンド一覧 (`just <task>`)

### 標準インターフェース

| コマンド | 用途 |
| --- | --- |
| `just check-env` | 必要ツール (uv, just, quarto, npm) の存在確認 |
| `just setup` | 依存インストール (`uv sync` + `npm install`) |
| `just check` | 品質ゲート (fmt + lint + typecheck + validate-docs + test) |
| `just check-full` | `check` + 実 HTML レンダリング |
| `just fix` | 自動修正 (fmt + lint + validate-docs --fix) |
| `just test` | pytest 実行 |
| `just clean` | ビルド成果物削除 (cross-platform) |

### Quarto

| コマンド | 用途 |
| --- | --- |
| `just docs` | プレビューサーバー (http://localhost:4312) |
| `just fix-docs` | プレビューが落ちない時の復旧 (Win/Mac/Linux 対応) |
| `just render-site` | HTML 実レンダリング |
| `just render-book-pdf` | PDF 実レンダリング |
| `just validate-docs` | ドキュメント整合性検証 |
| `just validate-docs-fix` | 自動修正可能なエラーを修正 |

### PDF 取り込み (用途別に選択)

| コマンド | 用途 | 必要な追加依存 |
| --- | --- | --- |
| `just extract-pdf <pdf>` | テキスト埋込済 PDF からテキスト+画像抽出 | (デフォルト) |
| `just extract-pdf-ocr <pdf>` | 画像 PDF (スキャン PDF) を OCR で読み取る | `uv sync --extra ocr` |
| `just extract-content <pdf> <start> <end>` | テキスト + 数式 (LaTeX) を抽出 | `uv sync --extra math` |
| `just render-pdf <pdf> <start> <end>` | PDF ページを PNG 化 | (デフォルト) |
| `just diagnose-pdf <pdf>` | PDF 構造診断 (テキスト埋込有無の確認) | (デフォルト) |

詳細は [`tools/README.md`](tools/README.md) を参照。

## オプション機能

依存をインストールして有効化:

```bash
uv sync --extra ocr        # 画像 PDF の OCR (easyocr, ~1GB)
uv sync --extra math       # 数式抽出 (pix2text, 大型 ML モデル)
uv sync --extra notebook   # numpy / matplotlib / jupyter
uv sync --extra quantum    # Qiskit
uv sync --extra shiny      # Shinylive 対話シミュレーション
uv sync --extra viz        # plotly / pyvis
uv sync --all-extras       # 全部入り
```

## 編集ワークフロー

1. `research/inbox/YYYY-MM-DD_topic/` に元素材 (写真・スキャン PDF・講義スライドなど) を置く
2. `just diagnose-pdf <pdf>` で PDF 構造を確認
3. テキスト埋込なし → `just extract-pdf-ocr`、ありなら `just extract-pdf`
4. `quarto/textbook/_NN_*.qmd` に内容を書き起こす
5. `just docs` でプレビュー、`just check` で品質確認
6. `git push` で GitHub Pages に自動公開

## AI エージェントとの協働

`AGENTS.md` に Claude Code / Codex / Gemini CLI 等向けの編集規約を記載しています。`AGENTS.md` を読ませた上でタスクを依頼してください。

## クレジット

このテンプレートは以下のプロジェクトの知見を統合して作成されました:

- [yama662607/Quantum-information](https://github.com/yama662607/Quantum-information) — ベース構成、validate_docs、pix2text 数式抽出
- [yukicomadaqq/peskin](https://github.com/yukicomadaqq/peskin) — easyocr による画像 PDF 対応、PDF 診断
- mechanics-class-simulation — Shinylive 統合、シンプル PDF 抽出
- Field-Theory — 標準ディレクトリ構成

## ライセンス

[MIT](LICENSE)
