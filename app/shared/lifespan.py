from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from redis.asyncio import from_url  # type: ignore

from app.infrastructure.db.session import async_engine, init_async_db

from .config import get_settings

# =============================================================================
# Creating Get Logger Instance.
# =============================================================================

logger = getLogger(__name__)


# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()


# =============================================================================
# FastAPI Lifespan Context.
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    # ---- Startup ----
    logger.info("Starting application...")

    # Create Redis client using RedisSettings.dsn
    redis = from_url(
        str(settings.redis.dsn),
        encoding="utf-8",
        decode_responses=True,
    )

    try:
        # Verify Redis connection
        await redis.ping()  # type: ignore
        app.state.redis = redis
        logger.info("Redis connected successfully.")

        # Initialize database (migrations, tables, etc.)
        await init_async_db()
        logger.info("Database initialized successfully.")

        yield

    except Exception as exc:
        logger.exception("Application startup failed.", exc_info=exc)
        raise

    finally:
        # ---- Shutdown ----
        logger.info("Shutting down application...")

        try:
            if hasattr(app.state, "redis"):
                await app.state.redis.close()
                logger.info("Redis connection closed.")
        except Exception as exc:
            logger.exception("Error closing Redis connection.", exc_info=exc)

        try:
            await async_engine.dispose()
            logger.info("Database engine disposed.")
        except Exception as exc:
            logger.exception("Error disposing database engine.", exc_info=exc)

        logger.info("Resources cleaned up successfully.")
