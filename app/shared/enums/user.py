from enum import StrEnum

# =============================================================================
# User Status Enums.
# =============================================================================


class UserStatusEnum(StrEnum):
    """
    Represents the lifecycle state of a user account.

    Members:
        PENDING: User has signed up but not yet verified.
        ACTIVE: User account is fully active.
        DEACTIVATED: User voluntarily deactivated their account.
        SUSPENDED: User is temporarily restricted by an administrator.
        BANNED: User is permanently blocked from the system.
    """

    PENDING = "pending"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    SUSPENDED = "suspended"
    BANNED = "banned"
