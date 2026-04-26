import os

import fitz


def check_first_pages():
    base_dir = "quarto/assets/pdf/preskill"
    pdfs = ["chap1.pdf", "chap2_15.pdf", "chap3_15.pdf", "chap4_01.pdf", "chap5_15.pdf"]

    for f in pdfs:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            continue
        doc = fitz.open(path)
        print(f"=== {f} (Total {doc.page_count} pages) ===")
        # 各ページの最初と最後の方を見て、ページ番号を探す
        for i in range(min(3, doc.page_count)):
            text = doc[i].get_text()
            print(f"--- PDF Page {i + 1} ---")
            # ページの上5行と下5行
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            print("TOP:", lines[:5])
            print("BOTTOM:", lines[-5:])
        doc.close()
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    check_first_pages()
