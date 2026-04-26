import shutil
from pathlib import Path


def clean():
    project_root = Path(__file__).parent.parent.resolve()

    # 削除対象のディレクトリとファイル
    targets = [
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        ".mypy_cache",
        "quarto/_freeze",
        "quarto/_output",
        "quarto/textbook-preskill/textbook_files",
        "quarto/textbook-watrous/textbook_files",
    ]

    print(" Cleaning artifacts...")

    for target_rel in targets:
        target_path = project_root / target_rel
        if target_path.exists():
            try:
                if target_path.is_dir():
                    shutil.rmtree(target_path)
                    print(f"Removed directory: {target_rel}")
                else:
                    target_path.unlink()
                    print(f"Removed file: {target_rel}")
            except Exception as e:
                print(f"Failed to remove {target_rel}: {e}")

    # 再帰的な __pycache__ と *.pyc の削除
    for p in project_root.rglob("__pycache__"):
        try:
            shutil.rmtree(p)
            print(f"Removed: {p.relative_to(project_root)}")
        except Exception:
            pass

    for p in project_root.rglob("*.pyc"):
        try:
            p.unlink()
            print(f"Removed: {p.relative_to(project_root)}")
        except Exception:
            pass

    print(" Cleanup complete!")


if __name__ == "__main__":
    clean()
