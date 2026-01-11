import click

from .admin_user import admin_user


@click.group()
def create() -> None:
    """Create something in db."""
    pass


create.add_command(admin_user)
