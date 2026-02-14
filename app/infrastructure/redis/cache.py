from logging import getLogger
from typing import Awaitable, Callable, cast

from pydantic import BaseModel
from redis.asyncio import Redis
from sqlmodel import SQLModel

# =============================================================================
# Redis Default Constants
# =============================================================================

DEFAULT_CACHE_TTL = 300

# =============================================================================
# Get Logger.
# =============================================================================


logger = getLogger(__name__)


# =============================================================================
# Redis Model Cache Class.
# =============================================================================


class RedisModelCache[T: BaseModel | SQLModel]:
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
        model: type[T],
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

    def _key(self, identifier: int | str) -> str:
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
        return f"cache:{self.namespace}:{identifier}"

    async def get(self, key: int | str) -> T | None:
        """
        Retrieve an object from the cache.

        The method:
        - Fetches raw JSON data from Redis
        - Validates and deserializes it into the configured model
        - Silently fails and returns `None` if data is invalid or corrupted

        Args:
            key:
                Unique identifier of the cached object.

        Returns:
            The deserialized model instance if found and valid,
            otherwise `None`.
        """
        raw = await self.redis.get(self._key(key))

        if raw is None:
            return None

        try:
            return cast(T, self.model.model_validate_json(raw))
        except Exception as exc:
            # Cache corruption or schema mismatch should never
            # break application flow.
            logger.debug("Cache data validation error: ", exc_info=exc)
            return None

    async def set(self, key: int | str, instance: T) -> None:
        """
        Store an object in Redis with expiration.

        The instance is serialized to JSON and stored using `SETEX`
        to ensure automatic expiration.

        Args:
            key:
                Unique identifier of the cached object.
            instance:
                Model instance to be cached.
        """
        await self.redis.setex(
            self._key(key),
            self.ttl,
            instance.model_dump_json(),
        )

    async def get_or_set(
        self, key: int | str, factory: Callable[[], Awaitable[T]]
    ) -> T:
        """
        Retrieve an object from cache or populate it if missing.

        This implements a classic *read-through cache* pattern:
        - Try cache first
        - If missing, call the async factory
        - Store the result in cache
        - Return the value

        Args:
            key:
                Unique identifier of the cached object.
            factory:
                Async callable that returns the model instance
                when the cache is empty.

        Returns:
            The cached or freshly created model instance.
        """
        cached = await self.get(key=key)
        if cached is not None:
            return cached

        instance = await factory()
        await self.set(key=key, instance=instance)
        return instance

    async def invalidate(self, key: int | str) -> None:
        """
        Remove a single object from the cache.

        This is typically called after an update or delete operation
        in the primary data store.

        Args:
            key:
                Unique identifier of the cached object.
        """
        await self.redis.delete(self._key(key))

    async def invalidate_many(self, keys: list[int | str]) -> None:
        """
        Remove multiple objects from the cache in a single Redis call.

        This method is optimized to avoid unnecessary Redis operations
        when the list of IDs is empty.

        Args:
            keys:
                List of object identifiers to invalidate.
        """
        if keys:
            await self.redis.delete(*(self._key(key) for key in keys))

    async def exists(self, key: int | str) -> bool:
        """
        Check whether a cache entry exists.

        Note:
            This does NOT validate the cached data, it only checks
            for key existence in Redis.

        Args:
            key:
                Unique identifier of the cached object.

        Returns:
            `True` if the key exists in Redis, otherwise `False`.
        """
        return bool(await self.redis.exists(self._key(key)))
