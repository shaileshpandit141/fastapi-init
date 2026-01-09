# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from db.models.bases import BaseIntIDModel

if TYPE_CHECKING:
    from models.role_permission_link import RolePermissionLink
    from models.user_role_link import UserRoleLink


class Role(BaseIntIDModel, table=True):
    __tablename__ = "roles"

    name: str = Field(max_length=50, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)

    users: list["UserRoleLink"] = Relationship(back_populates="role")
    permissions: list["RolePermissionLink"] = Relationship(back_populates="role")
