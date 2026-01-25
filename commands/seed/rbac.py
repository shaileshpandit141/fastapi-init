from click import command, echo, get_current_context

from .assign_permissions import assign_permissions
from .permissions import permissions
from .roles import roles

# ===== Run rbac system seed =====


@command()
def rbac() -> None:
    """Seed roles, permissions, and admin mappings."""

    # Get current context and invoke commands
    ctx = get_current_context()

    ctx.invoke(permissions)
    ctx.invoke(roles)
    ctx.invoke(assign_permissions)

    echo("RBAC bootstrap completed successfully.")
