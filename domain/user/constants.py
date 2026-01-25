from enum import Enum, StrEnum


class UserCache(Enum):
    NAMESPACE = "current:user"
    TTL = 300


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
