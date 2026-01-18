from datetime import datetime

from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from core.db.base import BaseIntIDModel, NonEmptyUpdateModel

from ..models.user import UserBase

# === User Schemas ===


class UserRead(UserBase, BaseIntIDModel):
    updated_at: datetime


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(NonEmptyUpdateModel):
    email: EmailStr | None = Field(default=None, max_length=255)
