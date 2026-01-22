# pyright: reportAssignmentType=false

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.models.base import BaseIntIDModel, BaseTimestampModel

if TYPE_CHECKING:
    from domain.role.models import Role

# === User Enums ===


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# === User SQLModels ===


class UserBase(SQLModel):
    email: EmailStr = Field(
        max_length=255, index=True, nullable=False, sa_column_kwargs={"unique": True}
    )
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)


class User(BaseIntIDModel, UserBase, BaseTimestampModel, table=True):
    __tablename__ = "users"

    password_hash: str = Field(max_length=255, nullable=False)

    roles: list["UserRole"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


# === Uer Role SQLModels ===


class UserRoleBase(SQLModel):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")
