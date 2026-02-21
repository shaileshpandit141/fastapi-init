from sqlalchemy import Column, Enum, String
from sqlmodel import Field, Relationship, SQLModel

from app.shared.enums._base import get_enum_values
from app.shared.enums.permission import PermissionEnum

from ._mixins import UUIDv7Mixin
from .role_permission import RolePermission

# =============================================================================
# Permission Base SQLModel.
# =============================================================================


class PermissionBase(SQLModel, table=False):
    code: PermissionEnum = Field(
        max_length=100,
        sa_column=Column(
            Enum(
                PermissionEnum,
                name="permission_enum",
                values_callable=get_enum_values,
            ),
            index=True,
            unique=True,
            nullable=False,
        ),
    )
    description: str = Field(
        max_length=255,
        sa_column=Column(
            String(255),
            nullable=False,
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
            "lazy": "selectin",
        },
    )
