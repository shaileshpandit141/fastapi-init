from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import create_engine

from core.config.settings import settings


def make_sync_url(async_url: str) -> str:
    return async_url.replace("+asyncpg", "").replace("+aiosqlite", "")


class EngineContainer:
    def __init__(self) -> None:
        self.sync_engine: Engine = create_engine(
            url=make_sync_url(settings.database_url),
            echo=settings.env == "dev",
            future=True,
        )

        self.async_engine: AsyncEngine = create_async_engine(
            url=settings.database_url,
            echo=settings.env == "dev",
            future=True,
        )


engines = EngineContainer()
