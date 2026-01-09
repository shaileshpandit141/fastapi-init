# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from db.models.bases import BaseIntIDModel

if TYPE_CHECKING:
    from models.role_permission_link import RolePermissionLink
    from models.user_role_link import UserRoleLink


class RoleBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)


class Role(BaseIntIDModel, RoleBase, table=True):
    __tablename__ = "roles"

    users: list["UserRoleLink"] = Relationship(back_populates="role")
    permissions: list["RolePermissionLink"] = Relationship(back_populates="role")
