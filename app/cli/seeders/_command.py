import click

from .permission import permissions

# =============================================================================
# Seed Data Command Group
# =============================================================================


@click.group()
def seed() -> None:
    """Seed initial data into the database."""
    pass


# =============================================================================
# Register sub commands to seed command.
# =============================================================================

seed.add_command(permissions)
