from core.db.base import NonEmptyUpdateModel

from ..models.user_role import UserRoleBase


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(NonEmptyUpdateModel):
    user_id: int | None = None
    role_id: int | None = None
