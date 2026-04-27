# Quarto 機能 → live demo 対応表

このテンプレに含まれる Quarto 機能を、どの partial で **動く例** として見られるかインデックス化したものです。「あの機能をどう書くんだっけ」と思ったらここから該当 partial に飛んでコピーしてください。

## Live demo の場所

各 partial は `quarto/textbook/textbook.qmd` から `{{< include >}}` で本に統合されており、`just docs` ローカルプレビューおよび GitHub Pages 公開先で実際に動作します。

| Partial | カバーする機能 |
| :--- | :--- |
| [`_03_interactive_demo.qmd`](../quarto/textbook/_03_interactive_demo.qmd) | matplotlib `FuncAnimation` + 日本語フォント (Pyodide) |
| [`_04_plotly_demo.qmd`](../quarto/textbook/_04_plotly_demo.qmd) | Plotly 静的 + アニメーション (`animation_frame`) (Pyodide) |
| [`_05_diagrams_and_math.qmd`](../quarto/textbook/_05_diagrams_and_math.qmd) | Mermaid (flow / sequence / state) / Graphviz `{dot}` / theorem 8 種 (`#thm-` `#def-` `#lem-` `#cor-` `#prp-` `#exm-` `#exr-` `#sol-`) / `.proof` div / 可換図式 (LaTeX `array` + Mermaid) / 数式 cross-ref (`@eq-`) |
| [`_06_layout_and_callouts.qmd`](../quarto/textbook/_06_layout_and_callouts.qmd) | `{.panel-tabset group="..."}` / Bootstrap grid (`{.grid}` + `{.g-col-N}`) / 5 種 callout (note / tip / warning / caution / important) / `appearance="simple"` `appearance="minimal"` / `collapse="true"` / カスタム CSS callout (`.field-notes` / `.important-point` — `templates/styles.css` 定義) |
| [`_07_figures_and_tables.qmd`](../quarto/textbook/_07_figures_and_tables.qmd) | subfigure (`layout-ncol=N`) / `.column-page` / `.column-margin` / `.aside` (inline) / lightbox gallery (`group="..."`) / pipe table / grid table / table cross-ref (`@tbl-`) |
| [`_08_text_and_citations.qmd`](../quarto/textbook/_08_text_and_citations.qmd) | code annotation (hover) `# <1>` / 脚注 `[^label]` / 定義リスト / blockquote / video (iframe; Quarto 1.8.x の `{{< video >}}` は既知バグで現状 iframe 推奨) / conditional content (`.content-visible when-format="..."`) / BibTeX 引用 (`@key`) / 自動参考文献 (`#refs` div) |

## 既存 templates/*.qmd (出発点スケルトン — 本には render されない)

新章を起こすときに `cp templates/foo.qmd quarto/textbook/_NN_xxx.qmd` してから書き始めるための雛形:

| ファイル | 用途 |
| :--- | :--- |
| `templates/quarto_feature_showcase.qmd` | 全機能盛り合わせ。reference として読みつつコピー元に |
| `templates/math_focused_template.qmd` | 数学・物理の章 (定理 + 証明 + 線形代数) の出発点 |
| `templates/textbook_template.qmd` | PDF 翻訳の Phase 1/2 ワークフロー雛形 (セクション断片) |
| `templates/theory_template.qmd` | V-S-V サイクル Theory フェーズのレッスン雛形 |

## 機能横断で参照される設定

| 設定 | 場所 | 役割 |
| :--- | :--- | :--- |
| `lightbox: auto` | `quarto/_quarto.yml` の `format.html` | 画像クリックで拡大 / `group=` でギャラリー |
| `bibliography: templates/references.bib` | `quarto/_quarto.yml` 直下 | BibTeX 引用元ファイル |
| `templates/references.bib` | — | 引用元 (knuth1984 / shannon1948 / landau1976 / nielsen2010 / einstein1905 / quarto2024) |
| `templates/styles.css` | `format.html.css` で読み込み | カスタム callout (`.field-notes` `.important-point` `.physics-notes`) や `.proof::after` 記号など |
| `pyodide.packages` | `textbook.qmd` の YAML | Pyodide ロード時に直列 install するパッケージ (race 回避) |

## 出力形式の出し分け

`.content-visible when-format="html"` / `.content-visible when-format="pdf"` / `.content-hidden when-format="..."` を使って HTML 専用 / PDF 専用の本文を切り分けられる。詳細は [`_08_text_and_citations.qmd`](../quarto/textbook/_08_text_and_citations.qmd) のセクション [@sec-conditional]。

## 関連ドキュメント

- [`docs/quarto-live.md`](quarto-live.md) — Pyodide (Quarto Live) 専門の動作レシピと既知 dead-end
- [`AGENTS.md`](../AGENTS.md) — AI agent 向けの規約 (qmd 編集の小刻みルール、ファイル分離、PDF 抽出ワークフロー)

## このテンプレを clone した利用者へ

1. `quarto/textbook/textbook.qmd` から個別 include 行を削れば該当 partial だけ非表示にできる
2. `templates/styles.css` の `.field-notes` の色とラベルを書き換えれば自分の分野色で独自 callout を作れる
3. `references.bib` は自分の文献に置換 / 追加。Quarto は CSL ファイル指定で APA / IEEE / MLA 等のスタイルに切替可能
