from datetime import datetime

from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from core.db.mixins import IntIDMixin
from core.db.schemas import AtLeastOneFieldModel

from .models import UserBase, UserRoleBase

# === User Schemas ===


class UserRead(UserBase, IntIDMixin):
    updated_at: datetime


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(AtLeastOneFieldModel):
    email: EmailStr | None = Field(default=None, max_length=255)


# === User Role Schemas ===


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(SQLModel):
    role_id: int


class UserRoleUpdate(AtLeastOneFieldModel):
    role_id: int | None = None


# === User Email Verification Otp Schemas ===


class EmailVerificationOTP(SQLModel):
    email: EmailStr
    otp: str


class SendEmailVerificationOTP(SQLModel):
    email: EmailStr
