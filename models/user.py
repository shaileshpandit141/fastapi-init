from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field

from db.mixins import IDMixin, TimestampMixin


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(IDMixin, TimestampMixin, table=True):

    __tablename__ = "users"

    email: EmailStr = Field(max_length=255, index=True, unique=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)
