from collections.abc import AsyncGenerator, Generator

import redis
import redis.asyncio as aioredis

from app.core.config import get_settings

# =============================================================================
# Creating Settings Instance.
# =============================================================================

redis_settings = get_settings().redis


# =============================================================================
# Async Redis Client.
# =============================================================================

async_redis = aioredis.Redis(
    host=redis_settings.HOST,
    port=redis_settings.PORT,
    db=redis_settings.DB,
    password=redis_settings.PASSWORD,
    ssl=redis_settings.SSL,
    socket_timeout=redis_settings.SOCKET_TIMEOUT,
    socket_connect_timeout=redis_settings.SOCKET_CONNECT_TIMEOUT,
    max_connections=redis_settings.MAX_CONNECTIONS,
    decode_responses=True,
)


# =============================================================================
# Sync Redis Client.
# =============================================================================

sync_redis = redis.Redis(
    host=redis_settings.HOST,
    port=redis_settings.PORT,
    db=redis_settings.DB,
    password=redis_settings.PASSWORD,
    ssl=redis_settings.SSL,
    socket_timeout=redis_settings.SOCKET_TIMEOUT,
    socket_connect_timeout=redis_settings.SOCKET_CONNECT_TIMEOUT,
    max_connections=redis_settings.MAX_CONNECTIONS,
    decode_responses=True,
)

# =============================================================================
# FastAPI Dependencies Functions
# =============================================================================


def get_sync_redis() -> Generator[redis.Redis, None, None]:
    yield sync_redis


async def get_async_redis() -> AsyncGenerator[aioredis.Redis, None]:
    yield async_redis
