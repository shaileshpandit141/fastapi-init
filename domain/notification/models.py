# pyright: reportAssignmentType=false

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, String, func
from sqlmodel import Field, SQLModel  # type: ignore

from core.db.mixins import UUIDv7Mixin
from core.utils.time import time

from .constants import NotificationEvent

# =============================================================================
# Notification Base SQLModel
# =============================================================================


class NotificationBase(SQLModel, table=False):
    title: str = Field(
        max_length=120,
        sa_column=Column(String(120), nullable=False),
    )
    message: str = Field(
        max_length=500,
        sa_column=Column(String(500), nullable=False),
    )
    event: NotificationEvent = Field(
        sa_column=Column(
            Enum(NotificationEvent, name="notification_event"), nullable=False
        )
    )
    is_read: bool = Field(default=False, index=True)
    is_deleted: bool = Field(default=False, index=True)

    def mark_as_read(self) -> None:
        """Mark notification as read."""
        if not self.is_deleted:
            self.is_read = True

    def mark_as_unread(self) -> None:
        """Mark notification as unread."""
        if not self.is_deleted:
            self.is_read = False

    def soft_delete(self) -> None:
        """Soft delete notification."""
        self.is_deleted = True
        self.is_read = True

    def restore(self) -> None:
        """Restore a soft-deleted notification."""
        self.is_deleted = False
        self.is_read = False


# =============================================================================
# Notification SQLModel
# =============================================================================


class Notification(UUIDv7Mixin, NotificationBase, table=True):
    __tablename__ = "notifications"

    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(
        default_factory=time.utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
        ),
    )
