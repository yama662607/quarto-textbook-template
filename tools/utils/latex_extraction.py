import argparse
import os
import sys


def extract_latex_from_images(image_paths, quiet=False):
    """
    Extracts LaTeX from a list of image paths using Pix2Text.
    Returns a list of strings (one per image).
    """
    results = []
    try:
        try:
            from pix2text import Pix2Text
        except ImportError:
            print(
                "pix2text is not installed. Run: uv sync --group math",
                file=sys.stderr,
            )
            return []

        p2t = Pix2Text(device="cpu")

        for img_path in image_paths:
            if not os.path.exists(img_path):
                if not quiet:
                    print(f"Warning: Image not found at {img_path}", file=sys.stderr)
                results.append("")
                continue

            # Recognition
            # recognized_text is a list of dicts or a single dict depending on version
            # Usually p2t.recognize(img_path) returns the full text with LaTeX
            res = p2t.recognize(img_path)
            # res is typically a string in the latest version or a list of elements
            if isinstance(res, str):
                results.append(res)
            else:
                # Merge elements if it's a list
                merged = "\n".join([item.get("text", "") for item in res])
                results.append(merged)

            if not quiet:
                print(f"--- Extracted LaTeX from {os.path.basename(img_path)} ---")
                print(results[-1])
                print("\n")
        return results
    except Exception as e:
        if not quiet:
            print(f"An error occurred during LaTeX extraction: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract LaTeX from images using Pix2Text.")
    parser.add_argument("image_paths", nargs="+", help="Paths to images")

    args = parser.parse_args()
    extract_latex_from_images(args.image_paths)
