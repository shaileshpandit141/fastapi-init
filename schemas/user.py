from datetime import datetime

from pydantic import BaseModel, EmailStr

from models.user import UserRole, UserStatus


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    status: UserStatus
    updated_at: datetime


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
