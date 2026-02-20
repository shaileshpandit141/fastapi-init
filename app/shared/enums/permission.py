from enum import StrEnum

# =============================================================================
# Permission Enums.
# =============================================================================


class PermissionEnum(StrEnum):
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
