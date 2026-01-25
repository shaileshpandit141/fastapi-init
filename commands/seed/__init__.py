import click

from .assign_roles_to_admin import assign_roles_to_admin
from .permissions import permissions
from .rbac import rbac
from .roles import roles


@click.group()
def seed() -> None:
    """Seed data into database."""
    pass


seed.add_command(roles)
seed.add_command(permissions)
seed.add_command(assign_roles_to_admin)
seed.add_command(rbac)
