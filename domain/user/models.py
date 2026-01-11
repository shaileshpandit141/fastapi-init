# pyright: reportAssignmentType=false

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from core.db.base import BaseIntIDModel, BaseTimestampModel

if TYPE_CHECKING:
    from domain.rbac.models import UserRoleLink


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255, index=True, unique=True, nullable=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE, nullable=False)


class User(BaseIntIDModel, UserBase, BaseTimestampModel, table=True):
    __tablename__ = "users"

    password_hash: str = Field(max_length=255, nullable=False)

    roles: list["UserRoleLink"] = Relationship(back_populates="user")
