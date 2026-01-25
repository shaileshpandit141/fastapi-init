from sqlmodel import SQLModel

from .engines import async_engine, engine


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


async def init_async_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
