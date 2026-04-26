import argparse
import os
import sys

# Add tools/utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))

try:
    from pdf_processing import extract_pdf_text
except ImportError:
    print("Error: Could not import pdf_processing from utils.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Extract text and LaTeX (OCR) from PDF pages.")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--start", type=int, default=1, help="Start page")
    parser.add_argument("--end", type=int, default=1, help="End page")
    parser.add_argument("--img_dir", default="/tmp", help="Directory containing rendered images")
    parser.add_argument("--no-latex", action="store_true", help="Skip LaTeX extraction")

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    # 1. Extract Text
    print(
        f" Extracting text from {os.path.basename(args.pdf_path)} (Pages {args.start}-{args.end})..."
    )
    texts = extract_pdf_text(args.pdf_path, args.start, args.end, quiet=True)

    # 2. Check for images and extract LaTeX
    latex_results = []
    image_paths = []

    for i in range(args.start, args.end + 1):
        img_path = os.path.join(args.img_dir, f"page_{i}.png")
        if os.path.exists(img_path):
            image_paths.append(img_path)
        else:
            print(f" Warning: Rendered image for page {i} not found at {img_path}.")
            print("   Please run 'just render-pdf' first if you need LaTeX OCR.")

    if not args.no_latex and image_paths:
        print(f" Extracting LaTeX via OCR from {len(image_paths)} images...")
        try:
            from latex_extraction import extract_latex_from_images

            latex_results = extract_latex_from_images(image_paths, quiet=True)
        except ImportError:
            print("Warning: latex_extraction not found in utils. Skipping LaTeX OCR.")

    # 3. Format Output
    for i in range(args.end - args.start + 1):
        curr_page = args.start + i
        print(f"\n{'=' * 50}")
        print(f"PAGE {curr_page}")
        print(f"{'=' * 50}")

        print("\n[TEXT]")
        if i < len(texts):
            print(texts[i].strip())
        else:
            print("(No text extracted)")

        if not args.no_latex:
            print("\n[MATH (LaTeX OCR)]")
            if i < len(latex_results):
                print(latex_results[i].strip())
            else:
                print("(No OCR result - image might be missing or extraction failed)")

        img_path = os.path.join(args.img_dir, f"page_{curr_page}.png")
        print(f"\n[IMAGE PATH]\n{img_path if os.path.exists(img_path) else '(Not found)'}")


if __name__ == "__main__":
    main()
