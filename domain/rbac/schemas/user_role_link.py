from core.db.base import NonEmptyUpdateModel
from domain.rbac.models import UserRoleLinkBase


class UserRoleLinkRead(UserRoleLinkBase):
    pass


class UserRoleLinkCreate(UserRoleLinkBase):
    pass


class UserRoleLinkUpdate(NonEmptyUpdateModel):
    user_id: int | None = None
    role_id: int | None = None
