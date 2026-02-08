from typing import Sequence
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions.http_exception import AlreadyExistsError
from core.repositories.exceptions import EntityConflictError

from .models import Notification
from .repositories import NotificationRepository
from .schemas import NotificationCreate

# =============================================================================
# Notification Service
# =============================================================================


class NotificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = NotificationRepository(model=Notification, session=session)

    async def create(self, data: NotificationCreate) -> Notification:
        try:
            notification = await self.repo.create(
                data=data,
            )
        except EntityConflictError:
            raise AlreadyExistsError("Notification already exists.")

        return notification

    async def list(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> Sequence[Notification]:
        permissions = await self.repo.find_by(
            conditions=[Notification.user_id == user_id]
        )

        return permissions

    async def get(self, notification_id: UUID) -> Notification:
        raise NotImplementedError

    async def mark_as_read(self, user_id: int, notification_id: UUID) -> Notification:
        raise NotImplementedError

    async def mark_all_as_read(
        self, user_id: int, notification_id: UUID
    ) -> Sequence[Notification]:
        raise NotImplementedError

    async def delete_read(self, user_id: int, notification_id: UUID) -> Notification:
        raise NotImplementedError
