from sqlalchemy.engine import Engine as SyncEngine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session as SyncSession
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connections import engines


class SessionFactories:
    def __init__(self, sync_engine: SyncEngine, async_engine: AsyncEngine) -> None:
        self.SyncSessionLocal = sessionmaker[SyncSession](
            bind=sync_engine,
            class_=SyncSession,
            autocommit=False,
            autoflush=False,
        )

        self.AsyncSessionLocal = async_sessionmaker[AsyncSession](
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


sessions = SessionFactories(
    sync_engine=engines.sync_engine,
    async_engine=engines.async_engine,
)
