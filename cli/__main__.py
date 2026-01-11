import click

from cli.create import create
from cli.seed import seed


@click.group()
def cli() -> None:
    """A command-line interface to manage FastAPI-Init app."""
    pass


cli.add_command(create)
cli.add_command(seed)

if __name__ == "__main__":
    cli()
