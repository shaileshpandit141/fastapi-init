from sqlmodel import SQLModel

from db.connections.engines import engines
from db.connections.sessions import sessions


async def init_db() -> None:
    async with engines.async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


__all__ = ["engines", "sessions", "init_db"]
