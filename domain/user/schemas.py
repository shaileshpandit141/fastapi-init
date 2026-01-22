from datetime import datetime

from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from core.db.models.base import BaseIntIDModel, NonEmptyUpdateModel

from .models import UserBase, UserRoleBase

# === User Schemas ===


class UserRead(UserBase, BaseIntIDModel):
    updated_at: datetime


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(NonEmptyUpdateModel):
    email: EmailStr | None = Field(default=None, max_length=255)


# === User Role Schemas ===


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(SQLModel):
    role_id: int


class UserRoleUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
