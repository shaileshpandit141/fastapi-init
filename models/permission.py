# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from db.models.bases import BaseIntIDModel

if TYPE_CHECKING:
    from models.role_permission_link import RolePermissionLink


class Permission(BaseIntIDModel, table=True):
    __tablename__ = "permissions"

    code: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)

    roles: list["RolePermissionLink"] = Relationship(back_populates="permission")
