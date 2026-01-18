# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

if TYPE_CHECKING:
    from .permission import Permission
    from .role import Role

# === Role Permission SQLModels ===


class RolePermissionBase(SQLModel):
    role_id: int = Field(foreign_key="roles.id", primary_key=True, index=True)
    permission_id: int = Field(
        foreign_key="permissions.id", primary_key=True, index=True
    )


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permissions"

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
