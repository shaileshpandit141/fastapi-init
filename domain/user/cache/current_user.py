from redis.asyncio import Redis

from infrastructure.cache.redis.base import BaseRedisCache

from ..constants.current_user import CACHE_NAMESPACE, CACHE_TTL
from ..models.user import User


class CurrentUserCache(BaseRedisCache[User]):
    def __init__(self, redis: Redis) -> None:
        super().__init__(
            model=User,
            redis=redis,
            namespace=CACHE_NAMESPACE,
            ttl=CACHE_TTL,
        )
