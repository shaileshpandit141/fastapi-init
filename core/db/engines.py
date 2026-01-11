from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import create_engine

from core.config.settings import settings


def make_sync_url(database_url: str) -> str:
    url = make_url(database_url)
    if url.drivername.startswith("postgresql+"):
        url = url.set(drivername="postgresql")
    elif url.drivername.startswith("sqlite+"):
        url = url.set(drivername="sqlite")
    return str(url)


class EngineFactories:
    def __init__(self) -> None:
        self.engine: Engine = create_engine(
            make_sync_url(settings.database_url),
            echo=settings.env == "dev",
        )

        self.async_engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=settings.env == "dev",
        )


engines = EngineFactories()
