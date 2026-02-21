import click

from .commands.create import create_user_command

# =============================================================================
# User management group.
# =============================================================================


@click.group(name="user")
def user_group() -> None:
    """Users management command."""
    pass


# =============================================================================
# Register sub commands to user group.
# =============================================================================

user_group.add_command(create_user_command, name="create")
