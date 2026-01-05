from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from redis.asyncio import from_url

from core.config.settings import settings
from db.connections import engines, init_db

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.redis = from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    logger.info("Redis Connected successfully.")
    try:
        await init_db()
        logger.info("Database initialized successfully.")
        yield
    finally:
        await app.state.redis.close()
        await engines.async_engine.dispose()
        logger.info("Resources have been cleaned up.")
