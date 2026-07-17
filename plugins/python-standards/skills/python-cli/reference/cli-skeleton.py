# Minimal complete typer application — the structure python-cli prescribes.
import logging
import sys
import tomllib
from pathlib import Path
from typing import Annotated

import typer
from platformdirs import user_config_dir

from example_tool.logging_config import configure_logging

app = typer.Typer(help="Example tool — one sentence of purpose.")
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(user_config_dir("example-tool")) / "config.toml"


def load_config() -> dict:
    """Config file is one layer of the precedence chain: flags > env > file > defaults."""
    if CONFIG_PATH.exists():
        return tomllib.loads(CONFIG_PATH.read_text())
    return {}


@app.callback()
def main(
    verbose: Annotated[bool, typer.Option("--verbose", help="Enable debug logging.")] = False,
) -> None:
    configure_logging(debug=verbose)


@app.command()
def convert(
    source: Annotated[Path, typer.Argument(help="File to convert.")],
    profile: Annotated[str | None, typer.Option(help="Profile name; falls back to config file.")] = None,
) -> None:
    """Convert SOURCE using the selected profile."""
    config = load_config()
    profile_name = profile or config.get("profile", "default")
    try:
        result = run_conversion(source, profile_name)
    except ExpectedToolError as exc:
        # Expected failure: one clear message, exit 1, no traceback.
        logger.error("%s", exc)
        raise typer.Exit(code=1) from exc
    # stdout carries DATA only — this line is pipeable output.
    typer.echo(result)


if __name__ == "__main__":
    app()
