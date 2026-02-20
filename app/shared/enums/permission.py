from ._base import LabeledEnum

# =============================================================================
# Permission Enums.
# =============================================================================


class PermissionEnum(LabeledEnum):
    USER_CREATE = ("user:create", "Create user")
    USER_UPDATE = ("user:update", "Update user")
    USER_DELETE = ("user:delete", "Delete user")
