import click

from .assign_permissions import assign_permissions
from .permissions import permissions
from .rbac import rbac
from .roles import roles


@click.group()
def seed() -> None:
    """Seed data into database."""
    pass


seed.add_command(permissions)
seed.add_command(roles)
seed.add_command(assign_permissions)
seed.add_command(rbac)
