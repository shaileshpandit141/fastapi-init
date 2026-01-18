from pydantic import BaseModel
from redis.asyncio import Redis
from sqlmodel import SQLModel

from .constants.cache_keys import BASE_REDIS_CACHE


class BaseRedisCache[Model: BaseModel | SQLModel]:
    """Type-safe Redis cache Base class."""

    __slots__ = ("_redis", "_namespace", "_model", "_ttl")

    def __init__(
        self, *, redis: Redis, namespace: str, model: str, ttl: int = BASE_REDIS_CACHE
    ) -> None:
        self._redis = redis
        self._namespace = namespace
        self._model = model
        self._ttl = ttl

    def _key(self, object_id: int | str) -> str:
        return f"cache:{self._namespace}:{self._model}:{object_id}"

    async def get(self, *, object_id: int | str, schema: Model) -> Model | None:
        raw = await self._redis.get(self._key(object_id))

        if raw is None:
            return None

        return schema.model_validate_json(raw)

    async def set(self, *, object_id: int | str, payload: Model) -> None:
        await self._redis.setex(
            self._key(object_id),
            self._ttl,
            payload.model_dump_json(),
        )

    async def invalidate(self, *, object_id: int | str) -> None:
        await self._redis.delete(self._key(object_id))

    async def invalidate_many(self, *, object_ids: list[int | str]) -> None:
        if not object_ids:
            return

        await self._redis.delete(*[self._key(obj_id) for obj_id in object_ids])
