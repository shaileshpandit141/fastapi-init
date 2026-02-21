import click

from .commands.permission import permission_command
from .commands.role import role_command
from .commands.sync_role_permission import sync_role_permission_command

# =============================================================================
# Seed data group.
# =============================================================================


@click.group()
def seed_group() -> None:
    """Seed initial data into the database."""
    pass


# =============================================================================
# Register sub commands to seed group.
# =============================================================================

seed_group.add_command(permission_command)
seed_group.add_command(role_command)
seed_group.add_command(sync_role_permission_command)
