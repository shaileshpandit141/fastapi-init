import click

from .permission import permissions
from .role import roles
from .sync_role_permission import sync_role_permission

# =============================================================================
# Seed Data Command Group
# =============================================================================


@click.group()
def seed_command() -> None:
    """Seed initial data into the database."""
    pass


# =============================================================================
# Register sub commands to seed command.
# =============================================================================

seed_command.add_command(permissions, name="permissions")
seed_command.add_command(roles, name="roles")
seed_command.add_command(sync_role_permission, name="sync-role-permission")
