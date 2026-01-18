from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.settings import settings

async_engine: AsyncEngine = create_async_engine(
    url=settings.database_url,
    echo=settings.env == "dev",
)
