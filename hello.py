"""Hello marimo 入門用ノート。"""

import marimo

__generated_with = "0.17.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    message = "Hello, marimo!"
    return (message,)


@app.cell
def _(message):
    print(message)
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
    return


if __name__ == "__main__":
    app.run()
