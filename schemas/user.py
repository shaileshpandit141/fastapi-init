from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from db.models.bases import BaseIntIDModel
from models.user import UserBase
from schemas.base import NonEmptyUpdateModel


class UserRead(BaseIntIDModel, UserBase):
    updated_at: datetime


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(NonEmptyUpdateModel):
    email: EmailStr | None = Field(default=None, max_length=255)
