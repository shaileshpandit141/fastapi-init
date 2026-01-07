from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from db.models.bases import BaseIntIDModel, BaseTimestampModel


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# ---- Core user model ----


class User(BaseIntIDModel, BaseTimestampModel, table=True):
    __tablename__ = "users"

    email: EmailStr = Field(max_length=255, index=True, unique=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)

    roles: list["UserRoleLink"] = Relationship(back_populates="user")


# ---- Role & permission models ----


class Role(BaseIntIDModel, table=True):
    __tablename__ = "roles"

    name: str = Field(max_length=50, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)

    users: list["UserRoleLink"] = Relationship(back_populates="role")
    permissions: list["RolePermissionLink"] = Relationship(back_populates="role")


class Permission(BaseIntIDModel, table=True):
    __tablename__ = "permissions"

    code: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)

    roles: list["RolePermissionLink"] = Relationship(back_populates="permission")


# ---- Link tables (many‑to‑many) ----


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(foreign_key="roles.id", primary_key=True)
    permission_id: int = Field(foreign_key="permissions.id", primary_key=True)

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
