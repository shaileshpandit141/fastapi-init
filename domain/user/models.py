# pyright: reportAssignmentType=false

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.models import BaseIntIDModel, BaseTimestampModel
from core.utils.time import time

from .constants import UserStatus

if TYPE_CHECKING:
    from domain.role.models import Role

# === User SQLModels ===


class UserBase(SQLModel):
    email: EmailStr = Field(
        max_length=255,
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True},
    )
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)


class EmailVerificationMixin(SQLModel):
    is_email_verified: bool = Field(default=False, nullable=False)
    email_verified_at: datetime | None = Field(default=None)

    def mark_email_verified(self) -> None:
        self.is_email_verified = True
        self.email_verified_at = time.utc_now()


class User(
    BaseIntIDModel,
    UserBase,
    EmailVerificationMixin,
    BaseTimestampModel,
    table=True,
):
    __tablename__ = "users"

    password_hash: str = Field(max_length=255, nullable=False)

    roles: list["UserRole"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def can_login(self) -> bool:
        return self.status == UserStatus.ACTIVE and self.is_email_verified


# === Uer Role SQLModels ===


class UserRoleBase(SQLModel):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")
