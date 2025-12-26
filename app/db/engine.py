from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

engine = create_async_engine(
    settings.async_db_url,
    echo=settings.env == "dev",
    future=True,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
