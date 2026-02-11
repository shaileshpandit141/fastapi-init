from typing import Sequence

from sqlmodel import desc

from core.repositories.repository import Repository as Repo
from core.repository.actions.insert import InsertMany
from core.repository.actions.select import SelectMany
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


class NotificationRepositoryEx(
    Repo[Notification, NotificationCreate, NotificationUpdate]
):
    pass
