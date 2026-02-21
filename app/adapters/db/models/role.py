from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, String
from sqlmodel import Field, Relationship, SQLModel

from app.shared.enums.role import RoleEnum

from ._mixins import UUIDv7Mixin
from .role_permission import RolePermission

if TYPE_CHECKING:
    from .user_role import UserRole

# =============================================================================
# Role Base SQLModel.
# =============================================================================


class RoleBase(SQLModel, table=False):
    name: RoleEnum = Field(
        sa_column=Column(
            Enum(
                RoleEnum,
                name="role_enum",
            ),
            index=True,
            unique=True,
            nullable=False,
        ),
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        sa_column=Column(
            String(255),
        ),
    )


# =============================================================================
# Role SQLModel.
# =============================================================================


class Role(RoleBase, UUIDv7Mixin, table=True):
    __tablename__ = "roles"  # type: ignore

    user_roles: list["UserRole"] = Relationship(back_populates="role")
    role_permissions: list["RolePermission"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
