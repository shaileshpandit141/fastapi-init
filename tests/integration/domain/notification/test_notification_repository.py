from uuid import UUID

import pytest

from domain.notification.constants import NotificationEvent
from domain.notification.repositories import NotificationRepository
from domain.notification.schemas import NotificationCreate


@pytest.mark.asyncio
@pytest.mark.integration
async def test_add_notifications(repo: NotificationRepository) -> None:
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
    await repo.session.commit()

    # Assertions
    assert len(results) > 0
    assert results[0].user_id == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_notifications(repo: NotificationRepository) -> None:
    results = await repo.list(user_id=1, limit=1, offset=0)

    # Assertions
    assert len(results) <= 1
    assert results[0].user_id == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_notification_by_id(repo: NotificationRepository) -> None:
    result = await repo.get_by_id(id=UUID("f0f3d6ca-cebe-4045-b255-cd531b573782"))

    # Assertion
    assert result is None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_notification_by_user_id(repo: NotificationRepository) -> None:
    result = await repo.get_by_user_id(1)

    # Assertion
    assert result.event == NotificationEvent.SYSTEM  # type: ignore


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mark_notification_as_read(repo: NotificationRepository) -> None:
    notification = await repo.get_by_user_id(1)
    updated_notification = await repo.make_as_read(notification)  # type: ignore

    # Assertion
    assert updated_notification.is_read is True


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mark_notification_as_unread(repo: NotificationRepository) -> None:
    notification = await repo.get_by_user_id(1)
    updated_notification = await repo.make_as_unread(notification)  # type: ignore

    # Assertion
    assert updated_notification.is_read is not True
