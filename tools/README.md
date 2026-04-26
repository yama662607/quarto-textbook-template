# tools/

各プロジェクト由来のスクリプトを **全て** 集めたディレクトリ。テンプレ利用時は不要なものを削除してください。

## 共通スクリプト (4プロジェクト統一)

| ファイル | 用途 | 出自 |
| --- | --- | --- |
| `check_env.py` | uv / just / quarto / npm の環境整合性チェック | Quantum-information |
| `clean.py` | ビルド成果物削除 (cross-platform, shutil ベース) | Quantum-information |
| `dev_server.py` | Quarto preview + watcher 起動 (port 4312) | Quantum-information |
| `validate_docs.py` | Quarto / Mermaid / LaTeX 整合性検証 + キャッシュ | Quantum-information |
| `kill_quarto_process.py` | Quarto preview プロセス停止 (Win/Mac/Linux 対応) | テンプレ独自 |

## PDF 抽出系 (用途で選定)

| ファイル | 用途 | 出自 | 依存 |
| --- | --- | --- | --- |
| `extract_pdf_simple.py` | テキスト埋込済 PDF からテキスト & 画像抽出 | mechanics-class-simulation | `pymupdf` |
| `extract_pdf_ocr.py` | **画像 PDF (テキスト未埋込) からも OCR で読取** | peskin | `pymupdf`, `easyocr` |
| `extract_pdf_content.py` | PDF からテキスト + 数式 (LaTeX) 抽出 | Quantum-information | `pymupdf`, `pix2text` |
| `render_pdf.py` | PDF ページを画像化 (シンプル) | Quantum-information | `pymupdf` |
| `render_pdf_peskin.py` | PDF ページを画像化 (peskin 版・diagnose 連携) | peskin | `pymupdf` |
| `diagnose_pdf.py` | PDF の構造診断 (テキスト埋込有無、ページ数等) | peskin | `pymupdf` |

## utils/

| ファイル | 用途 | 出自 |
| --- | --- | --- |
| `find_quarto.py` | quarto バイナリ探索 | Quantum-information |
| `quarto_watcher.py` | ファイル変更監視 | Quantum-information |
| `pdf_processing.py` | PDF 処理共通関数 | Quantum-information |
| `latex_extraction.py` | LaTeX 数式抽出ヘルパ | Quantum-information |
| `mermaid_parser.js` | Mermaid 図式パーサ (validate_docs.py から呼出) | Quantum-information / peskin |

## setup/ (Quantum-information プロジェクト固有)

Preskill 教科書 PDF の前処理スクリプト群。**汎用テンプレでは不要**、参考用に保持。

| ファイル | 用途 |
| --- | --- |
| `extract_pdf_image.py` | PDF → 画像変換 |
| `merge_preskill_pdf.py` | 複数 PDF のマージ |
| `check_preskill_first_pages.py` | ページ番号オフセット確認 |
| `investigate_preskill_pages.py` | ページ構造調査 |

## ルート直下の補助

| ファイル | 用途 | 出自 |
| --- | --- | --- |
| `mermaid_parser.js` | utils/ と同じ (peskin はルート配置) | peskin |

---

## tool 選定の指針

- **教科書 PDF をそのまま読み取りたい**: `extract_pdf_simple.py` (テキスト埋込済) → ダメなら `extract_pdf_ocr.py`
- **数式まで LaTeX で取り出したい**: `extract_pdf_content.py` (要 pix2text、重い)
- **PDF が画像のみ (スキャン PDF, 古い教科書)**: `extract_pdf_ocr.py` 必須
- **PDF を診断したい**: `diagnose_pdf.py` で構造確認 → 適切な extract を選ぶ
