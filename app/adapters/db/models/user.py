from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, Enum, String
from sqlmodel import Field, Relationship, SQLModel

from app.shared.datetime.utc_now import datetime, get_utc_now
from app.shared.enums._base import get_enum_values
from app.shared.enums.permission import PermissionEnum
from app.shared.enums.role import RoleEnum
from app.shared.enums.user import UserStatusEnum

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
            index=True,
            unique=True,
            nullable=False,
        ),
    )
    status: UserStatusEnum = Field(
        default=UserStatusEnum.PENDING,
        sa_column=Column(
            Enum(
                UserStatusEnum,
                name="user_status_enum",
                values_callable=get_enum_values,
            ),
            index=True,
            nullable=False,
        ),
    )

    def activate(self) -> None:
        self.status = UserStatusEnum.ACTIVE

    def suspend(self) -> None:
        self.status = UserStatusEnum.SUSPENDED

    def ban(self) -> None:
        self.status = UserStatusEnum.BANNED

    def deactivate(self) -> None:
        self.status = UserStatusEnum.DEACTIVATED


# =============================================================================
# User Model With Table.
# =============================================================================


class User(TimestampMixin, UserBase, UUIDv7Mixin, table=True):
    __tablename__ = "users"  # type: ignore

    is_email_verified: bool = Field(default=False, nullable=False)
    email_verified_at: datetime | None = Field(default=None)
    password_hash: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
        )
    )

    user_roles: list["UserRole"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin",
        },
    )

    def mark_email_verified(self) -> None:
        if self.is_email_verified:
            return

        self.is_email_verified = True
        self.email_verified_at = get_utc_now()

    @cached_property
    def role_names(self) -> set[str]:
        return {ur.role.name for ur in self.user_roles}

    def is_superadmin(self) -> bool:
        return RoleEnum.SUPERADMIN in self.role_names

    def has_role(self, role_name: RoleEnum) -> bool:
        if self.is_superadmin():
            return True

        return role_name in self.role_names

    @cached_property
    def permission_codes(self) -> set[PermissionEnum]:
        permissions: set[PermissionEnum] = set()

        for ur in self.user_roles:
            for rp in ur.role.role_permissions:
                permissions.add(rp.permission.code)

        return permissions

    def has_permission(self, permission: PermissionEnum) -> bool:
        if self.is_superadmin():
            return True

        return permission in self.permission_codes
