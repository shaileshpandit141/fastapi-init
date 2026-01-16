from sqlmodel import Field  # type: ignore

from core.db.base import NonEmptyUpdateModel
from domain.rbac.models.role import RoleBase

# === Role Schemas ===


class RoleRead(RoleBase):
    pass


class RoleCreate(RoleBase):
    pass


class RoleUpdate(NonEmptyUpdateModel):
    name: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)
