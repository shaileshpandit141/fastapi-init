import click

from commands.seeds.rbac import seed_rbac


@click.group()
def cli() -> None:
    """A command-line interface to manage FastAPI-Init app."""
    pass


cli.add_command(seed_rbac)
