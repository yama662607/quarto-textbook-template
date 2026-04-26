import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class QuartoWatcherHandler(FileSystemEventHandler):
    def __init__(self, project_root):
        self.project_root = Path(project_root).resolve()
        self.last_triggered = 0.0
        self.debounce_seconds = 1.0

        # マッピング定義: 変更検知ディレクトリ -> タッチすべきファイル
        self.chapter_map = {
            "chapter1": self.project_root / "quarto" / "textbook-preskill" / "textbook.qmd",
            "chapter2": self.project_root / "quarto" / "textbook-preskill" / "textbook.qmd",
            "chapter3": self.project_root / "quarto" / "textbook-preskill" / "textbook.qmd",
        }
        self.default_target = self.project_root / "quarto" / "index.qmd"

    def on_modified(self, event):
        if event.is_directory:
            return

        # 監視対象の拡張子を確認
        if not event.src_path.endswith(".qmd"):
            return

        src_path = Path(event.src_path).resolve()

        # ターゲットファイルの決定
        target_file = self._determine_target(src_path)

        # 自分自身への書き込みによる無限ループを避ける
        if target_file and src_path == target_file:
            return

        current_time = time.time()
        if current_time - self.last_triggered > self.debounce_seconds:
            if target_file:
                print(f"Detected change in {src_path.name}. Touching {target_file.name}...")
                self.touch_target(target_file)
            else:
                print(f"Detected change in {src_path.name}, but no specific target found.")

            self.last_triggered = current_time

    def _determine_target(self, src_path):
        """変更されたファイルのパスから、タッチすべきファイルを決定する"""
        try:
            # パスの中に "chapterX" が含まれているか探す
            parts = src_path.parts
            for part in parts:
                if part in self.chapter_map:
                    target = self.chapter_map[part]
                    if target.exists():
                        return target

            # デフォルト
            if self.default_target.exists():
                return self.default_target
            return None
        except Exception:
            return None

    def touch_target(self, target_file):
        # 複数回リトライしてファイルロックに対処する（特にWindows）
        max_retries = 3
        for i in range(max_retries):
            try:
                # 1文字追加して即座に削除することで、内容を変えずにmtimeを更新する
                with open(target_file, "a") as f:
                    f.write(" ")

                # Quartoが検知する時間を与える
                time.sleep(0.5)

                with open(target_file, "r+") as f:
                    content = f.read()
                    if content.endswith(" "):
                        f.seek(0)
                        f.truncate()
                        f.write(content[:-1])

                print(f"Successfully touched {target_file.name}.")
                return
            except Exception as e:
                print(f"Attempt {i + 1} failed to touch target file: {e}")
                time.sleep(0.5)

        print("Failed to touch target file after all retries.")


def main():
    # プロジェクトのルートディレクトリを基準にする
    project_root = Path(__file__).parent.parent.resolve()
    watch_path = project_root / "quarto"

    print("Starting Quarto Watcher...")
    print(f"Monitoring: {watch_path}")
    print("Mapping changes in chapter dirs to chapter.qmd files.")

    event_handler = QuartoWatcherHandler(project_root)
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
