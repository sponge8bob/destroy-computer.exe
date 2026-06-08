from typing import Annotated, Optional

import typer

from destroy_computer_exe import __version__
from destroy_computer_exe.games.wordle import play as play_wordle

app = typer.Typer(help="destroy-computer.exe — terminal DLE games", add_completion=False, no_args_is_help=False)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"destroy-computer.exe {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=_version_callback, is_eager=True, help="Show version"),
    ] = None,
) -> None:
    if ctx.invoked_subcommand is None:
        play_wordle()


@app.command()
def wordle() -> None:
    """Play Wordle — guess the 5-letter word in 6 tries."""
    play_wordle()
