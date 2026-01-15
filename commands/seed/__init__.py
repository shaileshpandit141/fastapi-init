import click

from .rbac import rbac


@click.group()
def seed() -> None:
    """Seed something in db."""
    pass


seed.add_command(rbac)
