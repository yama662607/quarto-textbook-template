"""PDFページを画像として書き出すツール。

スキャンPDFの内容を視覚的に確認するために使用する。
pymupdf を使ってPDFの各ページをPNG画像として出力する。
"""

import argparse
import sys
from pathlib import Path

import pymupdf


def render_pages(pdf_path, start_page=None, end_page=None, output_dir=None, dpi=200):
    """
    PDFの指定ページ範囲をPNG画像として出力する。

    Args:
        pdf_path (str): PDFファイルへのパス。
        start_page (int, optional): 開始ページ番号 (1-based)。
        end_page (int, optional): 終了ページ番号 (1-based)。
        output_dir (str, optional): 出力ディレクトリ。省略時は pdf と同じディレクトリ。
        dpi (int): 出力画像の解像度。デフォルト 200。
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

        # 出力ディレクトリの準備
        out = Path(output_dir) if output_dir else Path(pdf_path).parent / "rendered"
        out.mkdir(parents=True, exist_ok=True)

        zoom = dpi / 72  # 72 DPIがデフォルト
        mat = pymupdf.Matrix(zoom, zoom)

        print(f"📄 Rendering pages {start_idx + 1}-{end_idx} at {dpi} DPI ...")

        saved_files = []
        for i in range(start_idx, end_idx):
            page = doc[i]
            pix = page.get_pixmap(matrix=mat)
            filename = out / f"page_{i + 1:04d}.png"
            pix.save(str(filename))
            saved_files.append(filename)
            print(f"  ✅ Page {i + 1} → {filename}")

        doc.close()
        print(f"\n✨ {len(saved_files)} pages rendered to: {out}")
        return saved_files

    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDFページをPNG画像として書き出す。")
    parser.add_argument("pdf_path", help="PDFファイルへのパス")
    parser.add_argument("--start", type=int, help="開始ページ番号 (1-based)")
    parser.add_argument("--end", type=int, help="終了ページ番号 (1-based)")
    parser.add_argument("--output", "-o", help="出力ディレクトリ")
    parser.add_argument("--dpi", type=int, default=200, help="解像度 (デフォルト: 200)")

    args = parser.parse_args()
    render_pages(args.pdf_path, args.start, args.end, args.output, args.dpi)
