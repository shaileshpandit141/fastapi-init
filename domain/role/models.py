# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.mixins import IntIDMixin

if TYPE_CHECKING:
    from domain.permission.models import Permission
    from domain.user.models import UserRole

# === Role SQLModels ===


class RoleBase(SQLModel, table=False):
    name: str = Field(max_length=50, unique=True, index=True, nullable=False)
    description: str | None = Field(default=None, max_length=255)


class Role(IntIDMixin, RoleBase, table=True):
    __tablename__ = "roles"

    users: list["UserRole"] = Relationship(back_populates="role")
    permissions: list["RolePermission"] = Relationship(back_populates="role")


# === Role Permission SQLModels ===


class RolePermissionBase(SQLModel, table=False):
    role_id: int = Field(foreign_key="roles.id", primary_key=True, index=True)
    permission_id: int = Field(
        foreign_key="permissions.id", primary_key=True, index=True
    )


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permissions"

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
