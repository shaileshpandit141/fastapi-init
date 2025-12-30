from datetime import datetime, timezone
from typing import Any

from sqlalchemy import event
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapper
from sqlmodel import SQLModel

from core.settings import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.env == "dev",
    future=True,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# --- global timestamp events ---


@event.listens_for(SQLModel, "before_update", propagate=True)
def update_updated_at(
    mapper: Mapper[Any],
    connection: Connection,
    target: Any,
) -> None:
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)
