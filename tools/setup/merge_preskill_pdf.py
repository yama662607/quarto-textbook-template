import os

import fitz  # PyMuPDF
from PyPDF2 import PdfWriter


def get_page_info(pdf_path):
    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    # 最初と最後のページからテキストを抽出して、表記上のページ番号を推測する
    first_page_text = doc[0].get_text()
    last_page_text = doc[-1].get_text()
    doc.close()
    return page_count, first_page_text, last_page_text


def merge_pdfs(input_dir, output_path):
    # ファイル名から順番を特定する (chap1, chap2, ...)
    files = sorted(
        [f for f in os.listdir(input_dir) if f.startswith("chap") and f.endswith(".pdf")]
    )

    # chap10を最後、chap8-topologicalをchap8の場所に並び替えるなどの調整が必要
    # ここではシンプルに数値順にソート（ファイル名に含まれる数字で判定）
    def get_sort_key(filename):
        # "chap1.pdf" -> 1, "chap2_15.pdf" -> 2
        import re

        match = re.search(r"chap(\d+)", filename)
        if match:
            return int(match.group(1))
        return 999

    files.sort(key=get_sort_key)

    writer = PdfWriter()
    report = []
    current_page_offset = 1

    print(f"{'File':<25} | {'PDF Pages':<10} | {'Starting Global Page'}")
    print("-" * 60)

    for filename in files:
        path = os.path.join(input_dir, filename)
        page_count, first_text, last_text = get_page_info(path)

        writer.append(path)

        report.append(
            {
                "filename": filename,
                "pages": page_count,
                "start_global": current_page_offset,
            }
        )

        print(f"{filename:<25} | {page_count:<10} | {current_page_offset}")
        current_page_offset += page_count

    with open(output_path, "wb") as f:
        writer.write(f)

    return report


if __name__ == "__main__":
    input_dir = "quarto/assets/pdf/preskill"
    output_path = os.path.join(input_dir, "Preskill_Quantum_Computation_Full.pdf")

    # 既存の結合ファイルを削除（二重結合防止）
    if os.path.exists(output_path):
        os.remove(output_path)

    merge_pdfs(input_dir, output_path)
    print(f"\nCreated: {output_path}")
