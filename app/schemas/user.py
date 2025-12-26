from models.user import UserEmailBase, UserIdBase
from sqlmodel import Field


class UserListSchema(UserIdBase, UserEmailBase):
    pass


class UserCreateSchema(UserEmailBase):
    password: str = Field(max_length=255)
