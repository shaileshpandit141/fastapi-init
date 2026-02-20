from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.shared.enums.permission import PermissionEnum

from ._mixins import UUIDv7Mixin
from .role_permission import RolePermission

# =============================================================================
# Permission Base SQLModel.
# =============================================================================


class PermissionBase(SQLModel, table=False):
    code: PermissionEnum = Field(
        max_length=50,
        sa_column=Column(
            String(50),
            unique=True,
            index=True,
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
# Permission SQLModel.
# =============================================================================


class Permission(PermissionBase, UUIDv7Mixin, table=True):
    __tablename__ = "permissions"  # type: ignore

    role_permissions: list["RolePermission"] = Relationship(
        back_populates="permission",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
