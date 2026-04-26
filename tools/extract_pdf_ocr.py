"""スキャンPDFからOCRでテキストを抽出するツール。

pymupdf でページを画像化した後、easyocr でテキストを読み取る。
テキストレイヤーがあるPDFの場合は、そちらを優先的に使用する。
"""

import argparse
import sys
import textwrap

import pymupdf

# Windows等でのUnicodeEncodeErrorを防止
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# easyocr のリーダーキャッシュ（複数回呼び出し時の最適化）
_ocr_reader = None


def get_ocr_reader():
    global _ocr_reader
    if _ocr_reader is None:
        print("🔄 Loading OCR engine (first time may take a while)...", file=sys.stderr)
        import easyocr

        _ocr_reader = easyocr.Reader(["en"], gpu=False)
    return _ocr_reader


def extract_pdf_text(
    pdf_path,
    start_page=None,
    end_page=None,
    force_ocr=False,
    output_file=None,
    width=80,
):
    """
    PDFファイルから指定ページ範囲のテキストを抽出する。
    テキストレイヤーがない場合は easyocr でOCR処理を行う。

    Args:
        pdf_path (str): PDFファイルへのパス。
        start_page (int, optional): 開始ページ番号 (1-based)。
        end_page (int, optional): 終了ページ番号 (1-based)。
        force_ocr (bool): テキストレイヤーがあっても強制的にOCRを使用する。
        output_file (str, optional): 結果をファイルに保存するパス。
        width (int): テキスト折り返し幅。デフォルト80文字。
    """
    try:
        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)

        start_idx = max(0, (start_page or 1) - 1)
        end_idx = min(total_pages, end_page or total_pages)

        if start_idx >= total_pages:
            print(
                f"Error: Start page {start_page} is out of range (Total: {total_pages})",
                file=sys.stderr,
            )
            return

        # 出力先の準備
        out = open(output_file, "w", encoding="utf-8") if output_file else None

        def emit(text):
            """標準出力とファイルの両方に書き出す"""
            print(text)
            if out:
                out.write(text + "\n")

        emit(f"--- Extracting from {pdf_path} (Pages {start_idx + 1}-{end_idx}) ---")
        emit("")

        for i in range(start_idx, end_idx):
            page = doc[i]
            text = page.get_text().strip()

            emit(f"--- Page {i + 1} ---")

            if text and not force_ocr:
                # テキストレイヤーがある場合はそのまま使用
                for line in text.splitlines():
                    emit(line)
            else:
                # OCR処理
                reader = get_ocr_reader()

                # ページを高解像度の画像に変換
                zoom = 150 / 72  # 150 DPI
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img_bytes = pix.tobytes("png")

                # easyocr でテキスト抽出（各テキストブロックを個別に取得）
                results = reader.readtext(img_bytes, detail=0, paragraph=True)

                if results:
                    for paragraph in results:
                        # 長い行を折り返して読みやすくする
                        wrapped = textwrap.fill(paragraph, width=width)
                        emit(wrapped)
                        emit("")
                else:
                    emit("(No text detected on this page)")

            emit("")

        doc.close()
        if out:
            out.close()
            print(f"✅ Results saved to: {output_file}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDFファイルからテキストを抽出する（OCR対応）。")
    parser.add_argument("pdf_path", help="PDFファイルへのパス")
    parser.add_argument("--start", type=int, help="開始ページ番号 (1-based)")
    parser.add_argument("--end", type=int, help="終了ページ番号 (1-based)")
    parser.add_argument("--ocr", action="store_true", help="強制的にOCRを使用する")
    parser.add_argument("--output", "-o", help="結果をファイルに保存するパス")
    parser.add_argument(
        "--width",
        "-w",
        type=int,
        default=80,
        help="テキスト折り返し幅 (デフォルト: 80)",
    )

    args = parser.parse_args()
    extract_pdf_text(args.pdf_path, args.start, args.end, args.ocr, args.output, args.width)
