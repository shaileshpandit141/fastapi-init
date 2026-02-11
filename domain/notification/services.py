from typing import Sequence
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions.http_exception import AlreadyExistsError, NotFoundError
from core.repositories.exceptions import EntityConflictError

from .models import Notification
from .repositories import NotificationRepositoryEx
from .schemas import NotificationCreate, NotificationUpdate

# =============================================================================
# Notification Service
# =============================================================================


class NotificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = NotificationRepositoryEx(model=Notification, session=session)

    async def create(self, data: NotificationCreate, user_id: int) -> Notification:
        try:
            notification = await self.repo.create(
                data=data, values={"user_id": user_id}
            )
        except EntityConflictError:
            raise AlreadyExistsError("Notification already exists.")

        return notification

    async def list(
        self, notification_id: UUID, user_id: int, limit: int = 10, offset: int = 0
    ) -> Sequence[Notification]:
        notifications = await self.repo.find_by(
            conditions=[
                Notification.id == notification_id,
                Notification.user_id == user_id,
            ]
        )
        return notifications

    async def get(self, notification_id: UUID, user_id: int) -> Notification:
        notification = await self.repo.get_by(id=notification_id, user_id=user_id)
        if not notification:
            raise NotFoundError(detail="Notification not found.")

        return notification

    async def mark_as_read(self, notification_id: UUID, user_id: int) -> Notification:
        notification = await self.get(notification_id, user_id)
        notification = await self.repo.update(
            obj=notification, data=NotificationUpdate(is_read=True)
        )
        return notification

    async def mark_all_as_read(
        self, notification_id: UUID, user_id: int
    ) -> Sequence[Notification]:
        notifications = await self.list(notification_id, user_id)
        notifications = await self.repo.bulk_set(
            objs=notifications, data={"is_read": True}
        )
        return notifications

    async def delete(self, notification_id: UUID, user_id: int) -> None:
        notification = await self.get(notification_id, user_id)
        await self.repo.delete(obj=notification)
