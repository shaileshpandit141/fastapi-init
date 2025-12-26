from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


# User ID field shared by multiple schemas
class UserIdBase(SQLModel):
    id: None | int = Field(default=None, primary_key=True, index=True)


# User Email fields shared by multiple schemas
class UserEmailBase(SQLModel):
    email: str = Field(max_length=255)


# DB table model
class UserModel(UserIdBase, UserEmailBase, table=True):
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
