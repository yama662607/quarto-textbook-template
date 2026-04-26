"""PDFの構造を診断するスクリプト"""

import sys

import pymupdf

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "quarto/assets/peskin.pdf"
doc = pymupdf.open(pdf_path)

print(f"Total pages: {len(doc)}")
print(f"Metadata: {doc.metadata}")
print()

# 最初の5ページを詳しく調べる
for i in range(min(5, len(doc))):
    page = doc[i]
    text = page.get_text()
    images = page.get_images()
    print(f"--- Page {i + 1} ---")
    print(f"  Text length: {len(text)} chars")
    print(f"  Images count: {len(images)}")
    print(f"  Text preview: {repr(text[:200])}")
    print()

# 本文が始まりそうなページ(20-30)も調べる
for i in range(19, min(30, len(doc))):
    page = doc[i]
    text = page.get_text()
    images = page.get_images()
    print(f"--- Page {i + 1} ---")
    print(f"  Text length: {len(text)} chars")
    print(f"  Images count: {len(images)}")
    print(f"  Text preview: {repr(text[:200])}")
    print()

doc.close()
