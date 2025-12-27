from datetime import datetime
from enum import Enum
from uuid import UUID

from db.mixins import TimestampMixin, UUIDMixin
from sqlmodel import Field, SQLModel


# --- Enums ---


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# --- DB table model ---


class User(UUIDMixin, TimestampMixin, table=True):
    """Database model for storing users."""

    __tablename__ = "users"

    email: str = Field(max_length=255, index=True, nullable=False, unique=True)
    password_hash: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)


# --- Pydantic I/O schemas ---


class UserRead(SQLModel):
    """Schema for returning user info in responses."""

    id: UUID
    email: str
    role: UserRole
    status: UserStatus
    updated_at: datetime


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    email: str
    password: str


class UserUpdate(SQLModel):
    """Schema for updating user data."""

    email: str | None = None
