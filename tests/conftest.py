from typing import AsyncGenerator, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# =============================================================================
# Async Test DB URL
# =============================================================================


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# =============================================================================
# Async Test Engine Fixture
# =============================================================================


@pytest.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


# =============================================================================
# Async Test Swssion Fixture
# =============================================================================


@pytest.fixture
async def sessionx(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            yield cast(AsyncSession, session)
        finally:
            await session.rollback()
