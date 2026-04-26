import argparse
import sys

import fitz


def extract_pdf_image(pdf_path, page_num, out_path, dpi=300):
    """
    Extracts a specific page from a PDF and saves it as an image.
    This is useful for AI agents to visually read complex equations or diagrams
    using the view_file tool.
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        idx = page_num - 1  # Convert 1-based physical page to 0-based index
        if idx < 0 or idx >= total_pages:
            print(
                f"Error: Page {page_num} is out of range (Total pages: {total_pages})",
                file=sys.stderr,
            )
            return

        page = doc.load_page(idx)
        pix = page.get_pixmap(dpi=dpi)
        pix.save(out_path)
        print(f"Successfully saved page {page_num} to {out_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract a page from a PDF as an image for visual inspection"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("page", type=int, help="Page number to extract (1-based physical page)")
    parser.add_argument("out_path", help="Path to save the output image (e.g., /tmp/page_114.png)")
    parser.add_argument(
        "--dpi", type=int, default=300, help="DPI for the output image (default: 300)"
    )

    args = parser.parse_args()
    extract_pdf_image(args.pdf_path, args.page, args.out_path, args.dpi)
