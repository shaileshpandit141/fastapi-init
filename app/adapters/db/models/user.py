from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.core.time import datetime, get_utc_now
from app.shared.enums.permission import PermissionEnum
from app.shared.enums.role import RoleEnum
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

    @cached_property
    def _role_names(self) -> set[RoleEnum]:
        return {ur.role.name for ur in self.roles}

    def is_superadmin(self) -> bool:
        return RoleEnum.SUPERADMIN in self._role_names

    def has_role(self, role_name: RoleEnum) -> bool:
        if self.is_superadmin():
            return True

        return role_name in self._role_names

    @cached_property
    def _permission(self) -> set[PermissionEnum]:
        permissions: set[PermissionEnum] = set()

        for user_role in self.roles:
            for permission in user_role.role.permissions:
                permissions.add(permission.code)

        return permissions

    def has_permission(self, permission: PermissionEnum) -> bool:
        if self.is_superadmin():
            return True

        return permission in self._permission
