from sqlmodel import Field  # type: ignore

from core.db.base import BaseIntIDModel, NonEmptyUpdateModel
from domain.rbac.models import PermissionBase


class PermissionRead(PermissionBase, BaseIntIDModel):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(NonEmptyUpdateModel):
    code: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)
