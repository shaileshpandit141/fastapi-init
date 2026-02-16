# pyright: reportAssignmentType=false

from datetime import datetime
from enum import StrEnum

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel

from app.shared.get_utc_now import get_utc_now

from ..base import TimestampMixin, UUIDv7Mixin


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


# =============================================================================
# User Base Model.
# =============================================================================


class UserBase(SQLModel, table=False):
    email: EmailStr = Field(
        max_length=255,
        sa_column=Column(String(255), unique=True, index=True, nullable=False),
    )
    status: UserStatus = Field(default=UserStatus.PENDING, nullable=False)

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE

    def suspend(self) -> None:
        self.status = UserStatus.SUSPENDED

    def ban(self) -> None:
        self.status = UserStatus.BANNED

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE


# =============================================================================
# User Email Verification Model.
# =============================================================================


class UserEmailVerification(SQLModel, table=False):
    is_email_verified: bool = Field(default=False, nullable=False)
    email_verified_at: datetime | None = Field(default=None)

    def mark_email_verified(self) -> None:
        if self.is_email_verified:
            return

        self.is_email_verified = True
        self.email_verified_at = get_utc_now()


# =============================================================================
# User Model With Table.
# =============================================================================


class User(TimestampMixin, UserEmailVerification, UserBase, UUIDv7Mixin, table=True):
    __tablename__ = "users"

    password_hash: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
        )
    )
