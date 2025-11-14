"""Jupyter 変換デモ用 marimo ノート。"""

import marimo

__generated_with = "0.17.8"
app = mo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    title = "サンプル Jupyter 変換ノート"
    mo.md(f"## {title}")
    return


@app.cell
def _():
    x = 21
    y = x * 2
    return x, y


@app.cell
def _(mo, x, y):
    mo.md(f"""
    x = {x}, x * 2 = {y}
    """)
    return


if __name__ == "__main__":
    app.run()
