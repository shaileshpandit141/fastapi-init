from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .role import Role
    from .user import User

# =============================================================================
# User Role Base SQLModel.
# =============================================================================


class UserRoleBase(SQLModel, table=False):
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)


# =============================================================================
# User Role Relationship SQLModel.
# =============================================================================


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"  # type: ignore

    user: "User" = Relationship(
        back_populates="user_roles",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    role: "Role" = Relationship(
        back_populates="user_roles",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
