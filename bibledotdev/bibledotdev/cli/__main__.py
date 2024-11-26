from __future__ import annotations

import typer

from .verses import app as verses

app = typer.Typer()
app.add_typer(
    verses,
    name="verses",
)

if __name__ == "__main__":
    app()
