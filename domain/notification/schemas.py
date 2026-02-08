from core.db.mixins import UUIDv7Mixin
from core.db.schemas import AtLeastOneFieldModel

from .models import NotificationBase

# === Permission Schemas ===


class NotificationRead(NotificationBase, UUIDv7Mixin):
    pass


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(AtLeastOneFieldModel):
    is_read: bool = False
    is_deleted: bool = False
