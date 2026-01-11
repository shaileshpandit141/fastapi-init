from sqlmodel import Session, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .engines import engines


async def init_db() -> None:
    async with engines.async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


__all__ = ["init_db", "Session", "AsyncSession"]
