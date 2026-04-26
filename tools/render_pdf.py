import argparse
import os
import sys

# Add tools/utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))

try:
    from pdf_processing import extract_pdf_images
except ImportError:
    print("Error: Could not import pdf_processing from utils.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Render PDF pages as images (PNG).")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--start", type=int, default=1, help="Start page (1-based)")
    parser.add_argument("--end", type=int, default=1, help="End page (1-based)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for images")
    parser.add_argument("--out_dir", default="/tmp", help="Output directory for images")

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f" Rendering PDF pages {args.start}-{args.end} to {args.out_dir}...")
    image_paths = extract_pdf_images(
        args.pdf_path, args.start, args.end, out_dir=args.out_dir, dpi=args.dpi
    )

    if not image_paths:
        print(" Failed to render images.")
        sys.exit(1)

    print("\n Rendering complete. Saved images:")
    for path in image_paths:
        print(f" - {path}")


if __name__ == "__main__":
    main()
