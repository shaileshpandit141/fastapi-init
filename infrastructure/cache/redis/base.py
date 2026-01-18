from logging import getLogger
from typing import Awaitable, Callable

from pydantic import BaseModel
from redis.asyncio import Redis
from sqlmodel import SQLModel

from .constants.cache_keys import BASE_REDIS_CACHE

logger = getLogger(__name__)


class BaseRedisCache[Model: BaseModel | SQLModel]:
    """Type-safe Redis cache base class."""

    __slots__ = ("redis", "namespace", "model", "ttl")

    def __init__(
        self,
        *,
        model: type[Model],
        redis: Redis,
        namespace: str,
        ttl: int = BASE_REDIS_CACHE,
    ) -> None:
        self.model = model
        self.redis = redis
        self.namespace = namespace
        self.ttl = ttl

    def _key(self, id: int | str) -> str:
        return f"cache:{self.namespace}:{id}"

    async def get(self, *, id: int | str) -> Model | None:
        raw = await self.redis.get(self._key(id))

        if raw is None:
            return None

        try:
            return self.model.model_validate_json(raw)
        except Exception as exc:
            logger.debug("Cache data validation error: ", exc_info=exc)
            return None

    async def set(self, *, id: int | str, instance: Model) -> None:
        await self.redis.setex(
            self._key(id),
            self.ttl,
            instance.model_dump_json(),
        )

    async def get_or_set(
        self,
        *,
        id: int | str,
        factory: Callable[[], Awaitable[Model]],
    ) -> Model:
        cached = await self.get(id=id)
        if cached is not None:
            return cached

        instance = await factory()
        await self.set(id=id, instance=instance)
        return instance

    async def invalidate(self, *, id: int | str) -> None:
        await self.redis.delete(self._key(id))

    async def invalidate_many(self, *, ids: list[int | str]) -> None:
        if ids:
            await self.redis.delete(*(self._key(obj_id) for obj_id in ids))

    async def exists(self, *, id: int | str) -> bool:
        return bool(await self.redis.exists(self._key(id)))
