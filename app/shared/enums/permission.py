from ._base import LabeledEnum

# =============================================================================
# Permission Enums.
# =============================================================================


class PermissionEnum(LabeledEnum):
    """
    Represents application permissions used for Role-Based Access Control (RBAC).

    Permission format:
        <resource>:<action>

    Each member stores:
        value → Machine-readable permission code
        label → Human-readable description

    Permissions are assigned to roles.
    Roles are assigned to users.
    """

    # =============================================================================
    # USER PERMISSIONS
    # =============================================================================
    USER_CREATE = ("user:create", "Create a new user.")
    USER_READ = ("user:read", "View user details.")
    USER_LIST = ("user:list", "List and search users.")
    USER_UPDATE = ("user:update", "Update user information.")
    USER_DELETE = ("user:delete", "Permanently delete a user.")
    USER_RESTORE = ("user:restore", "Restore a soft-deleted user.")
    USER_SUSPEND = ("user:suspend", "Temporarily suspend a user.")
    USER_BAN = ("user:ban", "Permanently ban a user.")

    # =============================================================================
    # ROLE PERMISSIONS
    # =============================================================================
    ROLE_CREATE = ("role:create", "Create a new role.")
    ROLE_READ = ("role:read", "View role details.")
    ROLE_LIST = ("role:list", "List and search roles.")
    ROLE_UPDATE = ("role:update", "Update role information.")
    ROLE_DELETE = ("role:delete", "Delete a role.")
    ROLE_ASSIGN = ("role:assign", "Assign roles to users.")
    ROLE_REVOKE = ("role:revoke", "Revoke roles from users.")

    # =============================================================================
    # PERMISSION MANAGEMENT
    # =============================================================================
    PERMISSION_READ = ("permission:read", "View permission details.")
    PERMISSION_LIST = ("permission:list", "List and search permissions.")
    PERMISSION_ASSIGN = ("permission:assign", "Assign permissions to roles.")
    PERMISSION_REVOKE = ("permission:revoke", "Revoke permissions from roles.")
