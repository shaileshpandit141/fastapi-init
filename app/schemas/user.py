from models.user import UserEmailBase
from sqlmodel import Field


class UserReadSchema(UserEmailBase):
    is_superuser: bool


class CreateUserSchema(UserEmailBase):
    password: str = Field(
        min_length=8,
        max_length=72,
        description="bcrypt max length",
    )
