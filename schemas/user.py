from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

from models.user import UserRole, UserStatus

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
