import click

from commands.create import create
from commands.seed import seed


@click.group()
def cli() -> None:
    """A command-line interface to manage FastAPI-Init app."""
    pass


cli.add_command(create)
cli.add_command(seed)
