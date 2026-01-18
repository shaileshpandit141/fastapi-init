# pyright: reportAssignmentType=false

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

if TYPE_CHECKING:
    from domain.user.models.user import User

    from .role import Role

# === Uer Role SQLModels ===


class UserRoleBase(SQLModel):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")
