from datetime import datetime

from pydantic import BaseModel, EmailStr

from models.user import UserStatus


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    status: UserStatus
    updated_at: datetime


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
