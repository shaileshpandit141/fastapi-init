from sqlmodel import Field  # type: ignore

from core.db.mixins import IntIDMixin
from core.db.schemas import AtLeastOneFieldModel

from .models import PermissionBase

# === Permission Schemas ===


class PermissionRead(PermissionBase, IntIDMixin):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(AtLeastOneFieldModel):
    description: str | None = Field(default=None, max_length=255)
