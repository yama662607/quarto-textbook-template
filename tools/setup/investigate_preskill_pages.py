import os
import re

import fitz


def investigate_page_numbers():
    base_dir = "quarto/assets/pdf/preskill"
    files = sorted(
        [
            f
            for f in os.listdir(base_dir)
            if f.startswith("chap") and f.endswith(".pdf") and "Full" not in f
        ]
    )

    # chap番号順にソート
    def get_sort_key(filename):
        match = re.search(r"chap(\d+)", filename)
        if match:
            return int(match.group(1))
        return 999

    files.sort(key=get_sort_key)

    print(f"{'Filename':<25} | {'PDF Page 1 Text (Top/Bottom)'}")
    print("-" * 60)

    for filename in files:
        doc = fitz.open(os.path.join(base_dir, filename))
        # 最初のページの上部と下部のテキストをチェック
        text = doc[0].get_text()
        # ページ番号らしき数字を探す (独立した行の数字)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        page_num_hint = "Unknown"
        if lines:
            # 最初の3行または最後の3行を確認
            potential_nums = lines[:3] + lines[-3:]
            for s in potential_nums:
                if s.isdigit():
                    page_num_hint = s
                    break

        print(f"{filename:<25} | Hint: {page_num_hint}")
        doc.close()


if __name__ == "__main__":
    investigate_page_numbers()
