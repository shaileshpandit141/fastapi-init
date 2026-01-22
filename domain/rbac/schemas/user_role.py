from sqlmodel import SQLModel

from core.db.models.base import NonEmptyUpdateModel

from ..models.user_role import UserRoleBase

# === User Role Schemas ===


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(SQLModel):
    role_id: int


class UserRoleUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
