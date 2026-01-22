# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.models.base import BaseIntIDModel

if TYPE_CHECKING:
    from domain.role.models import RolePermission

# === Permission SQLModels ===


class PermissionBase(SQLModel):
    code: str = Field(max_length=50, unique=True, index=True, nullable=False)
    description: str | None = Field(default=None, max_length=255)


class Permission(BaseIntIDModel, PermissionBase, table=True):
    __tablename__ = "permissions"

    roles: list["RolePermission"] = Relationship(back_populates="permission")
