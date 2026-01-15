# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.base import BaseIntIDModel

if TYPE_CHECKING:
    from domain.user.models import User

# === Role SQLModels ===


class RoleBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)


class Role(BaseIntIDModel, RoleBase, table=True):
    __tablename__ = "roles"

    users: list["UserRole"] = Relationship(back_populates="role")
    permissions: list["RolePermission"] = Relationship(back_populates="role")


# === Permission SQLModels ===


class PermissionBase(SQLModel):
    code: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)


class Permission(BaseIntIDModel, PermissionBase, table=True):
    __tablename__ = "permissions"

    roles: list["RolePermission"] = Relationship(back_populates="permission")


# === Role Permission SQLModels ===


class RolePermissionBase(SQLModel):
    role_id: int = Field(foreign_key="roles.id", primary_key=True)
    permission_id: int = Field(foreign_key="permissions.id", primary_key=True)


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permissions"

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")


# === Uer Role SQLModels ===


class UserRoleBase(SQLModel):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")
