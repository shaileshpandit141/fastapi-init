import click

from .commands.create import create_user_command

# =============================================================================
# Seed Data Command Group
# =============================================================================


@click.group()
def user_command_group() -> None:
    """Users management command."""
    pass


# =============================================================================
# Register sub commands to seed command.
# =============================================================================

user_command_group.add_command(create_user_command, name="create")
