from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.core.time import datetime, get_utc_now
from app.shared.enums.user import UserStatus

from ._mixins import TimestampMixin, UUIDv7Mixin

if TYPE_CHECKING:
    from .user_role import UserRole

# =============================================================================
# User Base SQLModel.
# =============================================================================


class UserBase(SQLModel, table=False):
    email: EmailStr = Field(
        max_length=255,
        sa_column=Column(
            String(255),
            unique=True,
            index=True,
            nullable=False,
        ),
    )
    status: UserStatus = Field(
        default=UserStatus.PENDING,
        nullable=False,
    )

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE

    def suspend(self) -> None:
        self.status = UserStatus.SUSPENDED

    def ban(self) -> None:
        self.status = UserStatus.BANNED

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE


# =============================================================================
# User Email Verification SQLModel.
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
    __tablename__ = "users"  # type: ignore

    password_hash: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
        )
    )

    roles: list["UserRole"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
