from ._base import LabeledEnum

# =============================================================================
# Role Enums.
# =============================================================================


class RoleEnum(LabeledEnum):
    """
    Represents system roles used in Role-Based Access Control (RBAC).

    Roles group permissions together and are assigned to users.

    Role hierarchy (highest to lowest privilege):

        SUPERADMIN → Full system access.
        ADMIN      → Administrative privileges within managed scope.
        USER       → Standard authenticated user.

    Notes:
        - Roles are collections of permissions.
        - Authorization checks should always be permission-based.
        - SUPERADMIN may internally map to "system:manage".
    """

    SUPERADMIN = ("superadmin", "Full system access with unrestricted privileges.")
    ADMIN = ("admin", "Administrative role with elevated privileges.")
    USER = ("user", "Standard authenticated user with limited access.")
