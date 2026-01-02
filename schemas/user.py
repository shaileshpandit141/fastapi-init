from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from models.user import UserStatus


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    status: UserStatus
    updated_at: datetime


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
