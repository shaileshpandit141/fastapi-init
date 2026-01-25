from click import command, echo, get_current_context

from .assign_roles_to_admin import assign_roles_to_admin
from .permissions import permissions
from .roles import roles

# ===== Run rbac system seed =====


@command()
def rbac() -> None:
    """Seed roles, permissions, and admin mappings."""

    # Get current context and invoke commands
    ctx = get_current_context()

    ctx.invoke(roles)
    ctx.invoke(permissions)
    ctx.invoke(assign_roles_to_admin)

    echo("RBAC bootstrap completed successfully.")
