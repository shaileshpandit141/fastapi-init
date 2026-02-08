from typing import Sequence
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Notification
from .repositories import NotificationRepository
from .schemas import NotificationCreate, NotificationRead


class NotificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = NotificationRepository(model=Notification, session=session)

    async def create(self, data: NotificationCreate) -> NotificationRead:
        raise NotImplementedError

    async def list(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> Sequence[NotificationRead]:
        raise NotImplementedError

    async def get(self, notification_id: UUID) -> NotificationRead:
        raise NotImplementedError

    async def mark_as_read(
        self, user_id: int, notification_id: UUID
    ) -> NotificationRead:
        raise NotImplementedError

    async def mark_all_as_read(
        self, user_id: int, notification_id: UUID
    ) -> Sequence[NotificationRead]:
        raise NotImplementedError

    async def delete_read(
        self, user_id: int, notification_id: UUID
    ) -> NotificationRead:
        raise NotImplementedError
