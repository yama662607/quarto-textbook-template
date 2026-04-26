# Quarto Live (Pyodide) + 日本語フォント レシピ

ブラウザ内で動く Python シミュレーション ([Quarto Live](https://r-wasm.github.io/quarto-live/)) を
matplotlib + 日本語フォントと組合せて使うときの **動作確認済の手順** と、ハマりやすい落とし穴。

動作するサンプル: `quarto/textbook/_03_interactive_demo.qmd`

## 動作する組合せ

1. **拡張**: `quarto/_extensions/r-wasm/live/` を git で同梱 (`r-wasm/quarto-live`)
2. **フォント**: Noto Sans JP の **static Regular** TTF (5.3 MB) を `quarto/assets/fonts/NotoSansJP-Regular.ttf` に配置
   - DL URL: `https://fonts.gstatic.com/s/notosansjp/v56/-F6jfjtqLzI2JPCgQBnw7HFyzSD-AsregP8VFBEj75s.ttf`
   - 検証: `file quarto/assets/fonts/NotoSansJP-Regular.ttf` → `TrueType Font data, 19 tables, 1st "BASE"` が正解
3. **`_quarto.yml`**: `project.resources` に `assets/fonts/**/*` を追加してビルド時に `_book/` へコピーさせる
4. **qmd の YAML**: `filters: [r-wasm/live]`。Book project では `engine: markdown` も併記して jupyter 依存を回避。include 構造の場合は **親 qmd 側** に書く
5. **OJS スライダー**: `viewof x = Inputs.range([...], {label: tex\`...\`, value: ...})`
6. **Pyodide ブロック**: `#| autorun: true` + `#| input: ["x", "y", ...]` で reactive
7. **フォントロードのイディオム** (描画セルに **inline**):

```python
#| autorun: true
#| input: ["a", "b"]
import os
import warnings
import matplotlib
from matplotlib import font_manager
from pyodide.http import pyfetch

warnings.simplefilter("ignore")  # font 登録前後の Glyph missing 警告を抑制

if not os.path.exists("/tmp/NotoSansJP.ttf"):
    # ⚠️ pyfetch は **worker スクリプト** (/site_libs/quarto-contrib/...) を base に解決する。
    # ページ URL 基準ではない。`../../../` で 3 段戻ればルートに到達する
    # (extra `..` はルートで吸収されるので qmd の階層に関係なく安全)。
    resp = await pyfetch("../../../assets/fonts/NotoSansJP-Regular.ttf")
    with open("/tmp/NotoSansJP.ttf", "wb") as f:
        f.write(await resp.bytes())
font_manager.fontManager.addfont("/tmp/NotoSansJP.ttf")  # キャッシュ済でも毎回呼ぶ
matplotlib.rcParams["font.family"] = "Noto Sans JP"
matplotlib.rcParams["axes.unicode_minus"] = False

# --- ここから描画 ---
import numpy as np
import matplotlib.pyplot as plt
# ...
```

## 検証済 dead-end (やってはいけないこと)

| Don't | Why |
| --- | --- |
| `pyfetch("../assets/fonts/...")` のように `..` を qmd の階層に合わせて減らす | pyfetch は **worker base** に対して解決するのでページ階層は無関係。`../../../` で固定 |
| Font setup を `edit: false, autorun: true` の **別セルに分ける** | 描画セルとの実行順序が保証されず、最初のフレームで Glyph missing 警告が大量発生 |
| qmd YAML の `pyodide.resources` で font 指定 | Quarto Live の filter モードでは効かない (network タブで fetch されない) |
| `ojs_define(font_ready=True)` で OJS dependency を作って描画セルが待つ | 最初のロード時 OJS が未定義エラー (`font_ready is not defined`) を出して止まる |
| Variable font (`NotoSansJP[wght].ttf`、9.6 MB) を使う | Pyodide の matplotlib FreeType が parse できず `In TTFont: unknown file format` |
| `{pyodide}` セル内で `import shiny` / `import streamlit` | Pyodide では動かない。Quarto Live は素の numpy / matplotlib 中心 |
| OJS の `while + Promises.delay` ループでスライダーを高速更新して `{pyodide}` を毎フレーム再実行 | matplotlib 再描画 (>100ms / frame) が間隔に追いつかず描画が固まる。さらに Quarto Live 専用なので Jupyter / VSCode にコピーすると動かない |

## アニメーション

`matplotlib.animation.FuncAnimation` + `IPython.display.HTML(ani.to_jshtml())` を使う。
フレームを Python 側で全部計算 → JS プレイヤーとして埋め込まれるので:

- 再生 / 一時停止 / コマ送り / フレームスライダーが標準で付く
- 毎フレームの Pyodide 再実行が不要
- Jupyter / VSCode にコードをコピーしても同じように動く (Pyodide 固有なのは日本語フォントのロードだけ)

サンプル: `quarto/textbook/_03_interactive_demo.qmd` の FuncAnimation セクションを参照。

## 失敗時の典型症状と切り分け

- **`In FT2Font: Can not load face (unknown file format; error code 0x2)`**
  → 多くの場合 `pyfetch` が 404 を引いて HTML を TTF として読み込んでいる。
  preview のログで `(404: Not Found)` を grep し、`../../../` でルート相対になっているか確認
- **タイトルや軸ラベルが豆腐 (□)**
  → font が登録されていない。`addfont` を毎回呼んでいるか、`font.family` が `"Noto Sans JP"` か確認
- **編集しても変化しない**
  → include されるパーシャル (`_*.qmd`) は親 qmd を `touch` しないと preview が再レンダーしない場合がある。
  完全リセットは下記キャッシュクリア

## キャッシュトラブル時

```bash
rm -rf quarto/_book quarto/.quarto ~/Library/Caches/quarto
```
ブラウザは hard reload (Cmd+Shift+R)。
