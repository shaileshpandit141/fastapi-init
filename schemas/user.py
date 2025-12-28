from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.user import UserRole, UserStatus


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
    status: UserStatus
    updated_at: datetime


class UserCreateRequest(BaseModel):
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    email: str | None = None
