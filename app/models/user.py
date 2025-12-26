from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel
from utils.get_current_utc import get_current_utc

# ------------------------------
# Enums
# ------------------------------


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# ------------------------------
# DB table model
# ------------------------------


class User(SQLModel, table=True):
    """Database model for storing users."""

    id: int | None = Field(default=None, primary_key=True, index=True)

    # Shared fields
    email: str = Field(max_length=255, index=True, nullable=False, unique=True)
    password_hash: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=get_current_utc, nullable=False)
    updated_at: datetime = Field(
        default_factory=get_current_utc,
        nullable=False,
        sa_column_kwargs={"onupdate": get_current_utc},
    )


# ------------------------------
# Pydantic I/O schemas
# ------------------------------


class UserReadSchema(SQLModel):
    """Schema for returning user info in responses."""

    id: int
    email: str
    role: UserRole
    status: UserStatus
    updated_at: datetime


class CreateUserSchema(SQLModel):
    """Schema for creating a new user."""

    email: str
    password: str


class UpdateUserSchema(SQLModel):
    """Schema for updating user data."""

    email: str | None = None
