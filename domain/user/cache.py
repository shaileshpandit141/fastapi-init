from redis.asyncio import Redis

from infrastructure.cache.redis.base import BaseRedisCache

from .constants import UserCache
from .models import User


class CurrentUserCache(BaseRedisCache[User]):
    def __init__(self, redis: Redis) -> None:
        super().__init__(
            model=User,
            redis=redis,
            namespace=UserCache.NAMESPACE.value,
            ttl=UserCache.TTL.value,
        )
