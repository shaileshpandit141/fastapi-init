from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .permission import Permission
    from .role import Role

# =============================================================================
# Role Permission Base SQLModel.
# =============================================================================


class RolePermissionBase(SQLModel, table=False):
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True, index=True)
    permission_id: UUID = Field(
        foreign_key="permissions.id", primary_key=True, index=True
    )


# =============================================================================
# Role Permission Relationship SQLModel.
# =============================================================================


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permissions"  # type: ignore

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
