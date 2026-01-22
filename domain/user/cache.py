from redis.asyncio import Redis

from infrastructure.cache.abstractions.redis import BaseRedisCache

from .constants import CACHE_NAMESPACE, CACHE_TTL
from .models import User


class CurrentUserCache(BaseRedisCache[User]):
    def __init__(self, redis: Redis) -> None:
        super().__init__(
            model=User,
            redis=redis,
            namespace=CACHE_NAMESPACE,
            ttl=CACHE_TTL,
        )
