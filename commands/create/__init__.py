import click

from .superuser import superuser


@click.group()
def create() -> None:
    """Create some new data. (e.g: superuser, admin)"""
    pass


create.add_command(superuser)
