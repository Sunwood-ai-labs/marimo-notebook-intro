# はじめての marimo：Jupyter の次のノートブックを触ってみよう

marimo の基本コンセプト、セットアップ、そしてリアクティブ体験をこの README ひとつで学べます。情報量は入門記事と同じです。

---

## ゴール

読み終わるころには以下ができる状態を目指します。

* **Jupyter と marimo の違い**を把握する
* 自分の環境に **marimo をインストールして最初のノートブックを起動**する
* **UI ウィジェットの操作で依存セルだけが再計算される感覚**を掴む

ライトなハンズオンの指針として使ってください。

---

## marimo の概要

公式の説明（超訳）：

> Python 用の **リアクティブなノートブック**。ノートブックは `.py` ファイルで管理でき、セル間依存を解決して必要な部分だけを再実行し、スクリプトにも Web アプリにもなる。

([GitHub][marimo-github])

主な特徴：

* ✅ **ファイルはすべて `.py`** – `.ipynb` のような巨大 JSON ではないので Git diff が読みやすい
* ✅ **リアクティブ** – 上流の値が変わると依存セルだけ自動で再実行される([Marimo][marimo-docs])
* ✅ **実行順はセル位置ではなく依存関係ベース** – セルを並べ替えても壊れにくい
* ✅ **スクリプト／アプリとしても実行可能** – `python notebook.py` や `marimo run notebook.py` で動かせる([Marimo][marimo-quickstart])

Jupyter でありがちな「結局いまどのセルが最新？」問題を、**DAG（依存グラフ）＋自動再実行**で緩和してくれる設計です。([Marimo][marimo-docs])

---

## インストール

Python が入っていることを前提に、以下のどれかで導入します。

```bash
pip install marimo
```

SQL まわり（DuckDB / Polars）も一緒に入れる場合：

```bash
pip install "marimo[sql]"
```

環境マネージャとして `uv` を使う場合は、その場限りの実行も可能です。([Astral Docs][astral-uv])

```bash
uvx marimo edit
```

---

## 最初のノートブックを作る

### 1. エディタを開く

作業ディレクトリで次を実行します。

```bash
marimo edit hello.py
```

* 初回はブラウザで marimo UI が立ち上がります
* `hello.py` という **Python ファイル**が作られます([GitHub][marimo-cheat-sheet])
* このリポジトリにも `hello.py` を同梱してあるので、すぐに開いて試せます

### 2. 生成されるファイルの構造

```python
import marimo as mo

app = mo.App()

@app.cell
def _():
    import marimo as mo
    return mo


@app.cell
def _(mo):
    message = "Hello, marimo!"
    return message

@app.cell
def _(message):
    print(message)
    return

if __name__ == "__main__":
    app.run()
```

ポイント：

* `app = mo.App()` がノートブック全体を表す
* 先頭セルで `import marimo as mo` を呼び出して `mo` オブジェクトを後続セルに渡す
* `@app.cell` が 1 セルずつを表すデコレータ
* 関数の **引数名が依存関係** – 例では 2 個めのセルが `message` を受け取る
* `app.run()` がブラウザでのエントリーポイント

セルを増やすたびに `@app.cell` 関数が増え、marimo が依存関係を解析して実行順を決めます。([Marimo][marimo-docs])

---

## リアクティブ挙動のイメージ

Excel のセル参照に近いノリです。

1. セル A で `x = 10`
2. セル B で `y = x * 2`
3. セル C で `print(y)`

A を `x = 100` に書き換えると、marimo は依存グラフを見て B と C だけを再実行します。Jupyter のように順番を覚えておく必要がなく、状態の齟齬が起きづらいのがメリットです。([Marimo][marimo-docs])

---

## UI ウィジェットで遊ぶ

`marimo.ui`（慣習的に `mo.ui`）からウィジェットを作成できます。([Marimo][marimo-interactivity]) このリポジトリにはウィジェット専用のサンプル `ui_playground.py` を入れてあるので、`marimo edit ui_playground.py` を実行するとスライダー／テキスト入力／セレクトボックス／チェックボックスをまとめて試せます。以下はその一部抜粋です。

```python
@app.cell
def _(mo):
    slider = mo.ui.slider(start=0, stop=10, value=5, label="x の値")
    slider  # return しなくても最後に置くと UI として表示される
    return slider
```

結果表示セル：

```python
@app.cell
def _(slider, mo):
    x = slider.value
    mo.md(f"現在の x の値は **{x}** です")
    return
```

* `slider = mo.ui.slider(...)` で UI を生成
* `slider.value` でユーザーが選んだ値を参照
* スライダーを動かすと `slider` を引数に受け取るセルのみが再実行されます
* テキスト入力やセレクトボックスなど他の UI も同じ仕組みでリアクティブに連携できます（`ui_playground.py` 参照）
* 最初のセルで `import marimo as mo` を実行して `mo` を次のセルへ依存注入してください

この 2 セルを入れるだけで、簡単なダッシュボードのようなインタラクションが完成します。

---

## Jupyter との行き来

既存の `.ipynb` を試したい場合は変換コマンドを使います。([Marimo][marimo-quickstart]) このリポジトリには `notebooks/sample_analysis.ipynb` を用意してあるので、まずはそれをサンプルにすると手っ取り早いです。なお、**`marimo export ipynb` を使う際は事前に `nbformat` をインストール**しておいてください（例：`pip install nbformat` または `uv pip install nbformat`）。

```bash
# Jupyter → marimo (.py)
marimo convert notebooks/sample_analysis.ipynb -o notebooks/sample_analysis.py

# 変換したファイルを marimo で開く
marimo edit notebooks/sample_analysis.py
```

逆方向もワンコマンドです。

```bash
marimo export ipynb notebooks/sample_analysis.py -o notebooks/sample_analysis.ipynb
```

---

## 実行モードの使い分け

同じ `.py` を用途に応じて切り替えられます。([Marimo][marimo-quickstart])

```bash
# ノートブックとして編集
marimo edit analysis.py

# Web アプリとして配布
marimo run analysis.py

# バッチ／スクリプトとして実行
python analysis.py
```

1 つのファイルを「ノート＋アプリ＋スクリプト」として再利用できるのが気持ちいいポイントです。

---

## もっと勉強したくなったら

* 公式ドキュメントの **Getting Started** – インストールから基本概念まで順にまとまった入門ガイド([Marimo][marimo-getting-started])
* **Examples** ページ – スライダー、データフレーム、SQL などの断片サンプル集([Marimo][marimo-examples])
* `marimo-team/learn` – 線形代数や機械学習などを marimo ノートで学べる教材集([GitHub][marimo-learn])
* `marimo-cheat-sheet.py` – marimo 自体が marimo アプリとして動くチートシートで、定番パターンをすぐ参照可能([GitHub][marimo-cheat-sheet])

---

## 次のステップ

1. 手元で以下を実行し、UI が起動することを確認
   ```bash
   pip install marimo
   marimo edit hello.py
   ```
2. 上記のスライダー例を貼り付けて挙動を確かめる
3. 慣れてきたら既存の Jupyter ノート 1 本を `marimo convert` してみる

疑問や別用途の相談があれば、具体的なノートを貼ってもらえればリファクタやフロー設計も検討できます。

---

## このリポジトリでの動作確認状況

* `marimo edit hello.py` – 既定の 3 セルが起動し、`Hello, marimo!` の標準出力とスライダー → Markdown 更新が確認済み
* `marimo edit ui_playground.py` – スライダーと 2 倍計算セルがリアクティブに更新されることを確認済み
* `marimo run hello.py` / `marimo run ui_playground.py` – ブラウザ表示モードも問題なく立ち上がることを確認済み

必要に応じて、これらのファイルを編集して自分用のテンプレートにして構いません。

---

## まとめ

* **marimo は `.py` で書くリアクティブノートブック** – セルは `@app.cell` 付き関数、引数で依存を表現し、marimo が順序を決定([Marimo][marimo-docs])
* **状態管理がスマート** – 変わったセルに依存する部分のみが再実行され、「最新セルはどこ？」問題を軽減([Marimo][marimo-docs])
* **Git フレンドリーなプレーンテキスト** – 差分が追いやすく、モジュールやスクリプトとしても扱いやすい([Marimo][marimo-docs])
* **UI ウィジェット標準装備** – `mo.ui.*` を置くだけでリアクティブな UI が作れ、操作に合わせて必要セルだけが刷新([Marimo][marimo-docs])
* **Jupyter との往復も容易** – `marimo convert` / `marimo export` で行き来できる([GitHub][marimo-github])

---

## 参考リンク

### 公式系

* **marimo 公式サイト** – コンセプトや「次世代ノートブック」としての位置づけ([marimo.io][marimo-site])
* **Getting Started** – インストール、CLI、基本概念、チュートリアル([Marimo][marimo-getting-started])
* **公式ドキュメントトップ** – ハイライト機能やリアクティブ設計の背景([Marimo][marimo-docs])
* **GitHub (marimo-team/marimo)** – README で機能一覧やインストール手順、開発状況を確認([GitHub][marimo-github])
* **Pyodide ブログ記事** – ブラウザ完結実行やリアクティブ設計の背景解説([Pyodide blog][pyodide-marimo])

### 日本語記事

* **Qiita: 「jupyter notebookよりもMarimoが便利そう #Python」** – Jupyter との比較と体験談([Qiita][qiita-article])
* **Zenn: 「リアクティブなPythonノートブック環境『marimo』を試す」** – 日本語 README への導線と軽い使用例([Zenn][zenn-article])

### 英語記事

* **Real Python: 「marimo: A Reactive, Reproducible Notebook」** – 基本概念、リアクティブ挙動、UI コンポーネントを段階的に紹介([Real Python][realpython-article])
* **Medium: 「Can Marimo replace Jupyter notebooks?」** – Jupyter の弱点整理と marimo が解決する課題([Medium][medium-article])
* **DuckDB Docs: 「marimo Notebooks」** – DuckDB × marimo で SQL と Python を組み合わせるチュートリアル([DuckDB][duckdb-marimo])

---

これで「marimo 入門 README」は完成です。試してみて改善したいコードやワークフローが出てきたら、`hello.py` などを共有してください。一緒にブラッシュアップしましょう。

[marimo-docs]: https://docs.marimo.io/?utm_source=chatgpt.com "marimo"
[marimo-github]: https://github.com/marimo-team/marimo?utm_source=chatgpt.com "marimo-team/marimo: A reactive notebook for Python"
[marimo-site]: https://marimo.io/?utm_source=chatgpt.com "marimo | a next-generation Python notebook"
[marimo-getting-started]: https://docs.marimo.io/getting_started/?utm_source=chatgpt.com "Getting Started"
[marimo-quickstart]: https://docs.marimo.io/getting_started/quickstart/?utm_source=chatgpt.com "Quickstart"
[astral-uv]: https://docs.astral.sh/uv/guides/integration/marimo/?utm_source=chatgpt.com "Using uv with marimo"
[marimo-cheat-sheet]: https://github.com/vrtnis/marimo-cheat-sheet?utm_source=chatgpt.com "vrtnis/marimo-cheat-sheet"
[marimo-interactivity]: https://docs.marimo.io/guides/interactivity/?utm_source=chatgpt.com "Interactive elements"
[marimo-examples]: https://docs.marimo.io/examples/?utm_source=chatgpt.com "Examples"
[marimo-learn]: https://github.com/marimo-team/learn?utm_source=chatgpt.com "marimo-team/learn: 📚 A curated collection ..."
[pyodide-marimo]: https://blog.pyodide.org/posts/marimo/?utm_source=chatgpt.com "marimo: a reactive Python notebook that runs in the browser"
[qiita-article]: https://qiita.com/__Kat__/items/0970eb96d62f1ba9dc12?utm_source=chatgpt.com "jupyter notebookよりもMarimoが便利そう #Python"
[zenn-article]: https://zenn.dev/kun432/scraps/bdfe65535a3b22?utm_source=chatgpt.com "リアクティブなPythonノートブック環境「marimo」を試す"
[realpython-article]: https://realpython.com/marimo-notebook/?utm_source=chatgpt.com "marimo: A Reactive, Reproducible Notebook"
[medium-article]: https://medium.com/%40flyingjony/can-marimo-replace-jupyter-notebooks-fb8c7210ad35?utm_source=chatgpt.com "Can Marimo replace Jupyter notebooks?"
[duckdb-marimo]: https://duckdb.org/docs/stable/guides/python/marimo.html?utm_source=chatgpt.com "marimo Notebooks"
