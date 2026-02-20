from enum import StrEnum

# =============================================================================
# User Status Enums.
# =============================================================================


class UserStatus(StrEnum):
    """
    User Status Enums

    Fields:
        - PENDING: Just signed up, not verified yet.
        - ACTIVE: Fully active user.
        - INACTIVE: User chose to deactivate their account.
        - SUSPENDED: Temporarily blocked by admin.
        - BANNED: Permanently banned.
    """

    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
