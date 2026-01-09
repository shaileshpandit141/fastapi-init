# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from db.models.base import BaseIntIDModel

if TYPE_CHECKING:
    from models.role_permission_link import RolePermissionLink


class PermissionBase(SQLModel):
    code: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)


class Permission(BaseIntIDModel, PermissionBase, table=True):
    __tablename__ = "permissions"

    roles: list["RolePermissionLink"] = Relationship(back_populates="permission")
