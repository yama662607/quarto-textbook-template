# 引き継ぎメモ — Quarto Live (Pyodide) 統合の途中状態

> このファイルは作業中断時のスナップショット。Quarto Live (Pyodide) を
> テンプレに統合する作業が **未完了** で context 圧縮が必要になったため、
> 再開時に迷わず続きを進められるよう状況を記録する。
>
> **完成したらこのファイルは削除する。**

最終更新: 2026-04-26

## 全体ステータス

| プロジェクト | Quarto Live | 日本語フォント | デプロイ確認 |
| --- | --- | --- | --- |
| `~/Code/Learning/mechanics-class-simulation` | ✅ 動作確認済 | ✅ 完璧 (browser 確認済) | gh-pages 未試験 |
| `~/Code/Learning/quarto-textbook-template` | ⚠️ ファイルは揃ったがブラウザ動作未確認 | ⚠️ 未確認 | 未試験 |

## mechanics-class-simulation で確立したパターン (動作確認済)

### 1. 拡張ファイルの配置
- `quarto/_extensions/r-wasm/live/` に展開済
- `quarto/_extensions/quarto-ext/shinylive/` は削除

### 2. qmd の YAML
```yaml
---
title: "..."
filters:
  - r-wasm/live
---
```
- include されない単独ページ用のパターン
- include 構成の場合は親 qmd 側に書く (template ではこれが必要)

### 3. OJS スライダー
```ojs
viewof length = Inputs.range([0.1, 2.0], {step: 0.1, label: tex`\text{長さ } L`, value: 1.0})
```
- `tex` テンプレートリテラルで LaTeX ラベル
- アニメーションは `while` + `await Promises.delay(100)` ループ

### 4. Pyodide ブロック
```python
#| autorun: true
#| input: ["length", "initial_angle", "gravity", "time"]
# --- 日本語フォント (Noto Sans JP) のロード — 初回のみ ---
import os
import warnings
import matplotlib
from matplotlib import font_manager
from pyodide.http import pyfetch

warnings.simplefilter("ignore")  # font 登録前後の Glyph missing 警告を抑制

if not os.path.exists("/tmp/NotoSansJP.ttf"):
    resp = await pyfetch("../../../assets/fonts/NotoSansJP-Regular.ttf")
    with open("/tmp/NotoSansJP.ttf", "wb") as f:
        f.write(await resp.bytes())
font_manager.fontManager.addfont("/tmp/NotoSansJP.ttf")
matplotlib.rcParams["font.family"] = "Noto Sans JP"
matplotlib.rcParams["axes.unicode_minus"] = False

# --- 描画ロジック ---
import numpy as np
import matplotlib.pyplot as plt
# ...
```

### 5. 重要な「効かなかった」アプローチ
- ❌ font setup を `edit: false, autorun: true` の **別セルに分ける** → 順序保証されず警告大量発生
- ❌ qmd YAML に `pyodide.resources` で font 指定 → filter モードでは認識されない (ネットワークタブで fetch されない)
- ❌ `ojs_define(font_ready=True)` で OJS dependency 経由 → `font_ready is not defined` で OJS エラー
- ❌ Variable font (`NotoSansJP[wght].ttf` 9.6 MB) → Pyodide matplotlib FreeType が `In TTFont: unknown file format` で失敗
- ✅ **Static Regular font** を使うこと。URL: `https://fonts.gstatic.com/s/notosansjp/v56/-F6jfjtqLzI2JPCgQBnw7HFyzSD-AsregP8VFBEj75s.ttf` (5.3 MB)

### 6. `_quarto.yml` の追加
```yaml
project:
  resources:
    - "assets/fonts/**/*"   # font を _book/ に publish
```

## template で残っている課題

### 状況
- 拡張・font はコピー済 (mechanics と同じ static font 5.3 MB を `quarto/assets/fonts/NotoSansJP-Regular.ttf` に配置)
- `quarto/textbook/_03_interactive_demo.qmd` を新規追加 (sin 波シミュレーション、振幅/周波数/位相スライダー)
- `quarto/textbook/textbook.qmd` に `engine: markdown` + `filters: [r-wasm/live]` を追加
- `pyproject.toml` の `shiny` extra にコメント追加 (legacy 表示)
- AGENTS.md / README / CHANGELOG に Quarto Live 章追加済

### 未解決のブラウザ動作問題
最後に確認した時の症状:
- `http://localhost:4314/textbook/textbook.html` をレンダリングすると、Pyodide ブロックの出力エリアに
  `In TTFont: Cannot load face: 'unknown file format', error code 0x02`
  というエラーメッセージが描画される
- この問題は variable font が原因と推測して static font に置換したが、その確認の前に context 圧縮することになった
- preview server を立てて `http://localhost:4315/textbook/textbook.html` で再確認する必要あり

### 想定される追加修正
1. **font ファイルが正しく static 版か再確認**: `file quarto/assets/fonts/NotoSansJP-Regular.ttf`
   → `TrueType Font data, 19 tables, 1st "BASE"` が正解
2. **キャッシュクリア**: `rm -rf quarto/_book quarto/.quarto && rm -rf ~/Library/Caches/quarto`
3. **preview 再起動**: `cd ~/Code/Learning/quarto-textbook-template && QUARTO_PYTHON=$(pwd)/.venv/bin/python quarto preview quarto --port 4315`
4. **ブラウザで確認**: `http://localhost:4315/textbook/textbook.html` をリロード、autorun を 30〜40 秒待つ
5. それでもダメなら: pyfetch のパス `../assets/fonts/NotoSansJP-Regular.ttf` (qmd は textbook/_03_*.qmd で textbook.html 経由レンダリング → パスが正しいか curl で確認)

### include 構造での注意点
`textbook.qmd` から `{{< include _03_interactive_demo.qmd >}}` で取り込まれるが、
include 後は textbook.qmd のコンテキストでレンダリングされる。pyfetch のパスは
**HTML の URL を基準に解決される** ので、`http://host/textbook/textbook.html` から
`../assets/fonts/...` で `http://host/assets/fonts/...` を指す → これで正しいはず。

## 再開コマンド

```bash
# 1. 環境確認
cd ~/Code/Learning/quarto-textbook-template
just check        # コードは全パスするはず
file quarto/assets/fonts/NotoSansJP-Regular.ttf  # static font であることを確認

# 2. キャッシュクリア
rm -rf quarto/_book quarto/.quarto

# 3. preview 起動
QUARTO_PYTHON=$(pwd)/.venv/bin/python quarto preview quarto --port 4315 --no-browser

# 4. ブラウザで確認
# http://localhost:4315/textbook/textbook.html
# 30-40 秒待って Pyodide ブロックに sin 波が描画され、タイトルの日本語が
# 正しく表示されることを確認
```

## 完成後にやること

1. このファイル (`HANDOFF.md`) を削除
2. CHANGELOG の "Unreleased" セクションを 0.2.0 に昇格 (任意)
3. `gh repo create` で公開
4. mechanics-class-simulation で gh-pages デプロイのリハーサル

## 参考: 動作 OK のスクリーンショット (mechanics 側)

`~/Code/Learning/mechanics-class-simulation/.playwright-mcp/` 配下に保存:
- `with-jp-font-clean.png` — sample.qmd で日本語タイトル正常 + 警告なし
- `polar-final.png` — polar_kinematics.qmd で同上
