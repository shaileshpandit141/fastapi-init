from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from redis.asyncio import from_url  # type: ignore

from core.settings import settings

from .db import init_db
from .db.engines.async_engine import async_engine

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # ---- Startup ----
        app.state.redis = from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        logger.info("Redis Connected successfully.")

        await init_db()
        logger.info("Database initialized successfully.")

        yield

        # ---- Shutdown ----
    finally:
        await app.state.redis.close()
        await async_engine.dispose()
        logger.info("Resources have been cleaned up.")
