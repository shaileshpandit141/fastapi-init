from sqlmodel import SQLModel

from .engines.async_engine import async_engine


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


__all__ = ["init_db"]
