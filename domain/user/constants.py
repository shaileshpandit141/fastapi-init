from enum import Enum, StrEnum


class UserStatus(StrEnum):
    PENDING = "pending"  # Just signed up, not verified yet
    ACTIVE = "active"  # Fully active user
    INACTIVE = "inactive"  # User chose to deactivate their account
    SUSPENDED = "suspended"  # Temporarily blocked by admin
    BANNED = "banned"  # Permanently banned


class CurrentUserCacheConfig(Enum):
    NAMESPACE = "current:user"
    TTL = 300


class EmailVerificationOTPCacheConfig(Enum):
    NAMESPACE = "user:verification:email:otp"
    TTL = 300
