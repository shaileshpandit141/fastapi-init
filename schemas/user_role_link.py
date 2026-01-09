from models.user_role_link import UserRoleLinkBase
from schemas.base import NonEmptyUpdateModel


class UserRoleLinkRead(UserRoleLinkBase):
    pass


class UserRoleLinkCreate(UserRoleLinkBase):
    pass


class UserRoleLinkUpdate(NonEmptyUpdateModel):
    user_id: int | None = None
    role_id: int | None = None
