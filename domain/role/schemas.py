from pydantic import BaseModel
from sqlmodel import Field  # type: ignore

from core.db.models import BaseIntIDModel, NonEmptyUpdateModel

from .models import RoleBase, RolePermissionBase

# === Role Schemas ===


class RoleRead(RoleBase, BaseIntIDModel):
    pass


class RoleCreate(RoleBase):
    pass


class RoleUpdate(NonEmptyUpdateModel):
    name: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)


# === Role Permission Schemas ===


class RolePermissionRead(RolePermissionBase):
    pass


class RolePermissionCreate(BaseModel):
    permission_id: int


class RolePermissionUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
    permission_id: int | None = None
