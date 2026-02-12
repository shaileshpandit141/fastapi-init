import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from domain.notification.repositories import NotificationRepository


@pytest_asyncio.fixture(scope="function")
async def repo(async_session: AsyncSession) -> NotificationRepository:
    return NotificationRepository(async_session)
