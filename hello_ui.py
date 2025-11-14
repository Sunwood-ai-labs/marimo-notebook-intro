"""UI ウィジェット体験用の marimo ノートブック。"""

import marimo

__generated_with = "0.17.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    ## UI Playground
    下の各ウィジェットを触ると、依存しているセルだけが再実行される様子を確認できます。
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(start=0, stop=10, value=5, step=1, label="x の値")
    slider
    return (slider,)


@app.cell
def _(mo, slider):
    x = slider.value
    mo.md(f"現在の x の値は **{x}** です")
    return (x,)


@app.cell
def _(mo, x):
    doubled = x * 2
    mo.md(f"x を 2 倍すると **{doubled}** です")
    return


@app.cell
def _(mo):
    textbox = mo.ui.text(label="メモ", placeholder="任意のテキスト")
    textbox
    return (textbox,)


@app.cell
def _(mo, textbox):
    text = textbox.value or "(未入力)"
    mo.md(f"テキストボックスの値：`{text}`")
    return


@app.cell
def _(mo):
    choices = {"python": "Python", "sql": "SQL", "viz": "Visualization"}
    dropdown = mo.ui.dropdown(value="python", options=choices, label="得意分野")
    multiselect = mo.ui.multiselect(
        options=list(choices.values()),
        value=["Python"],
        label="興味あるトピック",
    )
    layout = mo.vstack([dropdown, multiselect])
    layout
    return dropdown, multiselect


@app.cell
def _(dropdown, mo, multiselect):
    choice = dropdown.value
    checked = ", ".join(multiselect.value) if multiselect.value else "(なし)"
    mo.md(
        f"選択中のメイン分野: **{choice}**  / チェック中: **{checked}**"
    )
    return


if __name__ == "__main__":
    app.run()
