from typing import Sequence

from core.repositories.repository import Repository as Repo
from core.repository.actions.insert import InsertMany
from core.repository.repository import Repository

from .models import Notification
from .schemas import NotificationCreate, NotificationUpdate

# from domain.user.models import User


# =============================================================================
# Notification Repository
# =============================================================================


class NotificationRepository(Repository):
    async def create_notifications(
        self, user_id: int, data: Sequence[NotificationCreate]
    ) -> Sequence[Notification]:
        return await self.execute(
            InsertMany(
                model=Notification,
                data=data,
                extra={"user_id": user_id},
            )
        )


class NotificationRepositoryEx(
    Repo[Notification, NotificationCreate, NotificationUpdate]
):
    pass
