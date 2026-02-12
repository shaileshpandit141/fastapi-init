from typing import Sequence
from uuid import UUID

from sqlmodel import desc

from core.repositories.repository import Repository as Repo
from core.repository.actions.insert import InsertMany
from core.repository.actions.save import Save
from core.repository.actions.select import SelectMany, SelectOne
from core.repository.repository import Repository

from .models import Notification
from .schemas import NotificationCreate, NotificationUpdate

# =============================================================================
# Notification Repository
# =============================================================================


class NotificationRepository(Repository):
    async def add(
        self, user_id: int, data: Sequence[NotificationCreate]
    ) -> Sequence[Notification]:
        return await self.execute(
            InsertMany(
                model=Notification,
                data=data,
                extra={"user_id": user_id},
            )
        )

    async def list(
        self, user_id: int, limit: int, offset: int
    ) -> Sequence[Notification]:
        return await self.execute(
            SelectMany(
                model=Notification,
                where=[Notification.user_id == user_id],
                order_by=[desc(Notification.created_at)],
                limit=limit,
                offset=offset,
            )
        )

    async def get_by_id(self, id: UUID) -> Notification | None:
        return await self.execute(
            SelectOne(
                model=Notification,
                where=[Notification.id == id],
            )
        )

    async def get_by_user_id(self, user_id: int) -> Notification | None:
        return await self.execute(
            SelectOne(
                model=Notification,
                where=[Notification.user_id == user_id],
            )
        )

    async def make_as_read(self, obj: Notification) -> Notification:
        obj.mark_as_read()
        return await self.execute(Save(obj))

    async def make_as_unread(self, obj: Notification) -> Notification:
        obj.mark_as_unread()
        return await self.execute(Save(obj))


class NotificationRepositoryEx(
    Repo[Notification, NotificationCreate, NotificationUpdate]
):
    pass
