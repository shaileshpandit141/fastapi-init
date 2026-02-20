from typing import Any

from sqlmodel import Field, Relationship, SQLModel

# =============================================================================
# Role Permission Base SQLModel.
# =============================================================================


class RolePermissionBase(SQLModel, table=False):
    role_id: int = Field(foreign_key="roles.id", primary_key=True, index=True)
    permission_id: int = Field(
        foreign_key="permissions.id", primary_key=True, index=True
    )


# =============================================================================
# Role Permission Relationship SQLModel.
# =============================================================================


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permissions"  # type: ignore

    role: Any = Relationship(back_populates="permissions")
    permission: Any = Relationship(back_populates="roles")
