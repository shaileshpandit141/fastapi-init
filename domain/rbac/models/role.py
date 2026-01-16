# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.base import BaseIntIDModel

if TYPE_CHECKING:
    from .role_permission import RolePermission
    from .user_role import UserRole

# === Role SQLModels ===


class RoleBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)


class Role(BaseIntIDModel, RoleBase, table=True):
    __tablename__ = "roles"

    users: list["UserRole"] = Relationship(back_populates="role")
    permissions: list["RolePermission"] = Relationship(back_populates="role")
