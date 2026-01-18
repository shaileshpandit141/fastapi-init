from logging import getLogger
from typing import Awaitable, Callable

from pydantic import BaseModel
from redis.asyncio import Redis
from sqlmodel import SQLModel

from ..constants.redis import DEFAULT_CACHE_TTL

logger = getLogger(__name__)


class BaseRedisCache[Model: BaseModel | SQLModel]:
    """
    Generic, type-safe Redis cache base class.

    This class abstracts common Redis caching operations for models that
    inherit from either `pydantic.BaseModel` or `sqlmodel.SQLModel`.

    It assumes:
    - JSON-based serialization (`model_dump_json`)
    - JSON-based deserialization (`model_validate_json`)
    - A single primary identifier (`id`) per cached object

    The class is intentionally minimal and designed to be extended or
    instantiated for specific domain models.
    """

    __slots__ = ("redis", "namespace", "model", "ttl")

    def __init__(
        self,
        *,
        model: type[Model],
        redis: Redis,
        namespace: str,
        ttl: int = DEFAULT_CACHE_TTL,
    ) -> None:
        """
        Initialize the Redis cache.

        Args:
            model:
                The Pydantic or SQLModel class used for validation and
                serialization/deserialization of cached data.
            redis:
                An instance of `redis.asyncio.Redis` used for all cache operations.
            namespace:
                A logical namespace used to isolate cache keys per model/domain.
                Example: "users", "articles", "sessions".
            ttl:
                Time-to-live (in seconds) for cached entries.
                Defaults to `BASE_REDIS_CACHE`.
        """
        self.model = model
        self.redis = redis
        self.namespace = namespace
        self.ttl = ttl

    def _key(self, id: int | str) -> str:
        """
        Build a fully-qualified Redis cache key.

        The key format is consistent and namespaced to avoid collisions
        across different cache domains.

        Example:
            cache:users:42

        Args:
            id:
                Unique identifier of the cached object.

        Returns:
            A Redis-compatible string key.
        """
        return f"cache:{self.namespace}:{id}"

    async def get(self, *, id: int | str) -> Model | None:
        """
        Retrieve an object from the cache.

        The method:
        - Fetches raw JSON data from Redis
        - Validates and deserializes it into the configured model
        - Silently fails and returns `None` if data is invalid or corrupted

        Args:
            id:
                Unique identifier of the cached object.

        Returns:
            The deserialized model instance if found and valid,
            otherwise `None`.
        """
        raw = await self.redis.get(self._key(id))

        if raw is None:
            return None

        try:
            return self.model.model_validate_json(raw)
        except Exception as exc:
            # Cache corruption or schema mismatch should never
            # break application flow.
            logger.debug("Cache data validation error: ", exc_info=exc)
            return None

    async def set(self, *, id: int | str, instance: Model) -> None:
        """
        Store an object in Redis with expiration.

        The instance is serialized to JSON and stored using `SETEX`
        to ensure automatic expiration.

        Args:
            id:
                Unique identifier of the cached object.
            instance:
                Model instance to be cached.
        """
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
        """
        Retrieve an object from cache or populate it if missing.

        This implements a classic *read-through cache* pattern:
        - Try cache first
        - If missing, call the async factory
        - Store the result in cache
        - Return the value

        Args:
            id:
                Unique identifier of the cached object.
            factory:
                Async callable that returns the model instance
                when the cache is empty.

        Returns:
            The cached or freshly created model instance.
        """
        cached = await self.get(id=id)
        if cached is not None:
            return cached

        instance = await factory()
        await self.set(id=id, instance=instance)
        return instance

    async def invalidate(self, *, id: int | str) -> None:
        """
        Remove a single object from the cache.

        This is typically called after an update or delete operation
        in the primary data store.

        Args:
            id:
                Unique identifier of the cached object.
        """
        await self.redis.delete(self._key(id))

    async def invalidate_many(self, *, ids: list[int | str]) -> None:
        """
        Remove multiple objects from the cache in a single Redis call.

        This method is optimized to avoid unnecessary Redis operations
        when the list of IDs is empty.

        Args:
            ids:
                List of object identifiers to invalidate.
        """
        if ids:
            await self.redis.delete(*(self._key(obj_id) for obj_id in ids))

    async def exists(self, *, id: int | str) -> bool:
        """
        Check whether a cache entry exists.

        Note:
            This does NOT validate the cached data, it only checks
            for key existence in Redis.

        Args:
            id:
                Unique identifier of the cached object.

        Returns:
            `True` if the key exists in Redis, otherwise `False`.
        """
        return bool(await self.redis.exists(self._key(id)))
