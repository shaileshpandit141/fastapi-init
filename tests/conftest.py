from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.db.session import get_async_session
from app.main import app

# =============================================================================
# Async Test DB URL.
# =============================================================================

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# =============================================================================
# Async Test Engine Fixture.
# =============================================================================


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


# =============================================================================
# Async Test Session Fixture.
# =============================================================================


@pytest_asyncio.fixture(scope="function")
async def async_session(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()


# =============================================================================
# Test Client Fixture.
# =============================================================================


@pytest.fixture
async def client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    async def get_async_test_session() -> AsyncGenerator[AsyncSession, Any]:
        yield async_session

    app.dependency_overrides[get_async_session] = get_async_test_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()
