from app.adapters.db.models._mixins import UUIDv7Mixin, TimestampMixin
from app.adapters.db.models.user import UserBase


class UserRead(TimestampMixin, UserBase, UUIDv7Mixin):
    pass
