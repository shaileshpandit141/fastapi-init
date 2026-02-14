from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.config import get_settings

settings = get_settings()


# =============================================================================
# Async and Sync Engines
# =============================================================================


async_engine = create_async_engine(
    url=settings.db.async_dsn,
    echo=settings.app.DEBUG,
    pool_pre_ping=True,
)

sync_engine = create_engine(
    url=settings.db.sync_dsn,
    echo=settings.app.DEBUG,
    pool_pre_ping=True,
)


# =============================================================================
# Async and Sync Sessions
# =============================================================================


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# =============================================================================
# Database Initializer Functions
# =============================================================================


async def init_async_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def init_sync_db() -> None:
    with sync_engine.begin():
        SQLModel.metadata.create_all(sync_engine)


# =============================================================================
# Async and Sync Dependencies
# =============================================================================


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_session() -> Generator[Session, None, None]:
    with SyncSessionLocal() as session:
        yield session
