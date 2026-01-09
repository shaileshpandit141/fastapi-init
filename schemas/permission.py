from sqlmodel import Field

from db.models.bases import BaseIntIDModel
from models.permission import PermissionBase
from schemas.base import NonEmptyUpdateModel


class PermissionRead(BaseIntIDModel, PermissionBase):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(NonEmptyUpdateModel):
    code: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)
