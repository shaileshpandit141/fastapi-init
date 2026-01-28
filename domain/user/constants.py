from enum import Enum, StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CurrentUserCacheConfig(Enum):
    NAMESPACE = "current:user"
    TTL = 300


class EmailVerificationOTPCacheConfig(Enum):
    NAMESPACE = "user:verification:email:otp"
    TTL = 300
