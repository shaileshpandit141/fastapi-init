from enum import Enum

from sqlmodel import Field

from db.mixins import TimestampMixin, UUIDMixin


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(UUIDMixin, TimestampMixin, table=True):

    __tablename__ = "users"

    email: str = Field(max_length=255, index=True, nullable=False, unique=True)
    password_hash: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)
