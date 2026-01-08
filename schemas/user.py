from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel

from models.user import UserStatus


class UserRead(SQLModel):
    id: int
    email: EmailStr
    status: UserStatus
    updated_at: datetime


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(SQLModel):
    email: EmailStr | None = None


class RolePermissionCreate(SQLModel):
    role_id: int
    permission_id: int
