from core.db.models.base import NonEmptyUpdateModel

from ..models.user_role import UserRoleBase

# === User Role Schemas ===


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(NonEmptyUpdateModel):
    user_id: int | None = None
    role_id: int | None = None
