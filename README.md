# Quarto Textbook Template

[![Quality Checks](https://github.com/yama662607/quarto-textbook-template/actions/workflows/check.yml/badge.svg)](https://github.com/yama662607/quarto-textbook-template/actions/workflows/check.yml)
[![Quarto Publish](https://github.com/yama662607/quarto-textbook-template/actions/workflows/publish.yml/badge.svg)](https://github.com/yama662607/quarto-textbook-template/actions/workflows/publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made with Quarto](https://img.shields.io/badge/Made%20with-Quarto-39729E)](https://quarto.org)

Quarto Book で教科書・講義ノート・演習資料を作り、GitHub Pages に公開するためのテンプレートです。本文サンプル、章テンプレート、Quarto 機能例、ブラウザ内 Python シミュレーションを最初から含めています。

## Quick Start

GitHub の **Use this template** から新しいリポジトリを作り、clone します。

```bash
git clone https://github.com/<you>/<your-repo>.git
cd <your-repo>
```

初回セットアップ:

```bash
# macOS / Linux
./scripts/bootstrap.sh

# Windows PowerShell
.\scripts\bootstrap.ps1
```

既に `uv` / `bun` / `just` / `quarto` が入っている場合:

```bash
just setup
just docs
```

プレビューは [http://localhost:4312](http://localhost:4312) で開きます。同じ Wi-Fi の端末からは `http://<your-lan-ip>:4312/` でも確認できます。

## まず見るページ

`just docs` 後、トップページから以下へ移動できます。

| ページ | 用途 |
| --- | --- |
| ホーム | テンプレート全体の入口 |
| 導線サンプル | qmd を追加した後に sidebar とホームへ置く例 |
| 章テンプレート一覧 | 教材・演習・理論ノートなどの書き方サンプル |
| ワークフロー | 素材取り込みから公開までの運用手順 |
| 本文サンプル | 実際の textbook 構成 |
| 教材本編サンプル内の機能例 | Mermaid、表、引用、Quarto Live、Plotly、シミュレーションなど |
| 論文精読ガイド | `docs/paper-deep-dive.md` と `quarto/examples/paper-deep-dive-page.qmd` |

## このテンプレートに含まれるもの

- Quarto Book の HTML / PDF 出力
- GitHub Pages 自動公開
- Quarto Live + Pyodide によるブラウザ内 Python 実行
- matplotlib / Plotly の対話シミュレーション例
- Mermaid、Graphviz、KaTeX、引用、list table などのサンプル
- 論文を精読教科書に変える編集ガイド
- PDF 取り込み補助ツール
- `just check` による品質確認
- AI エージェント向け編集規約 (`AGENTS.md`)

Quarto の新しめの機能や採用判断は [`docs/quarto-modern.md`](docs/quarto-modern.md) にまとめています。

## 書き換える場所

新しい教材として使うときは、まず以下を自分のプロジェクト向けに変更します。

| ファイル | 変更内容 |
| --- | --- |
| `quarto/_quarto.yml` | タイトル、著者、リポジトリ URL、footer |
| `quarto/index.qmd` | ホームの説明、主要ページへの導線 |
| `quarto/textbook/textbook.qmd` | 本文に含める章の構成 |
| `quarto/textbook/_*.qmd` | 各章の本文 |
| `package.json`, `pyproject.toml` | プロジェクト名・説明 |
| `README.md` | 派生先プロジェクトの説明 |
| `LICENSE`, `.github/CODEOWNERS`, `SECURITY.md` | 所有者情報 |

本文は `quarto/textbook/textbook.qmd` に集約し、章は `_01_*.qmd` のような partial に分けて `{{< include >}}` で読み込みます。

qmd を追加したら、ページを作るだけで終わらせず、ホームと sidebar の導線も更新します。

| 追加するもの | 最短手順 |
| --- | --- |
| 単独ページ | qmd を作る → `quarto/_quarto.yml` の `book.chapters` に追加 → `quarto/index.qmd` のロードマップ表にリンクを追加 → `just docs` でホーム / sidebar / 前後ナビを確認 |
| 本文 partial | `quarto/textbook/_NN_topic.qmd` を作る → `quarto/textbook/textbook.qmd` に include を追加 → ホームから飛ばしたい見出しに `{#sec-id}` を付ける → `quarto/index.qmd` から `textbook/textbook.qmd#sec-id` へリンク |

具体例は `quarto/example-map.qmd` と `quarto/examples/` を見てください。

## よく使うコマンド

| コマンド | 用途 |
| --- | --- |
| `just setup` | 依存関係をインストール |
| `just docs` | ローカルプレビュー |
| `just check` | 品質チェック |
| `just fix` | 自動修正 |
| `just render-site` | HTML を実レンダリング |
| `just render-book-pdf` | PDF をレンダリング |
| `just clean` | ビルド成果物を削除 |
| `just quarto-capabilities` | 現在の Quarto で使える機能を確認 |

`just docs` と render/check 系コマンドは同時に実行できません。Quarto の出力競合を避けるため、テンプレート側でロックしています。

## PDF から教材を作る場合

PDF やスキャン画像から qmd を作るときは、必ず画像確認と文字抽出を併用します。

```bash
just diagnose-pdf <pdf>
just render-pdf <pdf> <start> <end>
just extract-pdf <pdf> <start> <end>
```

抽出されたテキストだけで書き起こさず、生成された PNG を見ながら式、図表、ページ対応を確認してください。詳しくは [`AGENTS.md`](AGENTS.md) と [`tools/README.md`](tools/README.md) を参照してください。

## 公開

GitHub Pages を使う場合:

1. GitHub の Settings -> Pages を開く
2. Source を `gh-pages` branch に設定
3. `main` に push する

push 後、`.github/workflows/check.yml` と `.github/workflows/publish.yml` が走ります。

## 構成

```text
quarto/                  # Quarto ソース
  index.qmd              # ホーム
  example-map.qmd        # qmd 追加後の導線サンプル
  examples/              # 単独ページ配置の最小例
  template-catalog.qmd   # 章テンプレート一覧
  workflow-guide.qmd     # 運用ワークフロー
  textbook/              # 本文サンプル
  templates/             # CSS / HTML / qmd テンプレート
  assets/                # 画像・PDF・フォント
docs/                    # 補足ドキュメント
  paper-deep-dive.md     # 論文精読教科書の編集ガイド
tools/                   # 開発支援 Python ツール
tests/                   # pytest
Justfile                 # 統一コマンド
AGENTS.md                # AI エージェント向け規約
```

## クレジット

- [Quarto Live](https://github.com/r-wasm/quarto-live) - ブラウザ内 Python 実行
- [Noto Sans JP](https://github.com/notofonts/noto-cjk) - Pyodide matplotlib 用日本語フォント

このテンプレートは、関連する Quarto 教材プロジェクトで得た運用知見を統合して作成しています。

## ライセンス

[MIT](LICENSE)
