import pytest

from core.repository.actions.insert import AsyncSession
from domain.notification.constants import NotificationEvent
from domain.notification.repositories import NotificationRepository
from domain.notification.schemas import NotificationCreate


@pytest.mark.asyncio
@pytest.mark.integration
async def test_add_notifications(
    async_session: AsyncSession,
) -> None:
    repo = NotificationRepository(async_session)
    results = await repo.add(
        user_id=1,
        data=[
            NotificationCreate(
                title="Welcome to the platform",
                message="Your account has been successfully created.",
                event=NotificationEvent.SYSTEM,
            ),
            NotificationCreate(
                title="Password Reset Requested",
                message="Click the link to reset your password.",
                event=NotificationEvent.COMMENT,
            ),
        ],
    )
    await async_session.commit()

    # Assertions
    assert len(results) > 0
    assert results[0].user_id == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_notifications(
    async_session: AsyncSession,
) -> None:
    repo = NotificationRepository(async_session)
    results = await repo.list(user_id=1, limit=1, offset=0)

    # Assertions
    assert len(results) <= 1
    assert results[0].user_id == 1
