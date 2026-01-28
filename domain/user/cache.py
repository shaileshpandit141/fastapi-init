from redis.asyncio import Redis

from infrastructure.cache.redis.base import BaseRedisCache

from .constants import CurrentUserCacheConfig, EmailVerificationOTPCacheConfig
from .models import User
from .schemas import EmailVerificationOTP


class CurrentUserCache(BaseRedisCache[User]):
    def __init__(self, redis: Redis) -> None:
        super().__init__(
            model=User,
            redis=redis,
            namespace=CurrentUserCacheConfig.NAMESPACE.value,
            ttl=CurrentUserCacheConfig.TTL.value,
        )


class EmailVerificationOTPCache(BaseRedisCache[EmailVerificationOTP]):
    def __init__(self, redis: Redis) -> None:
        super().__init__(
            model=EmailVerificationOTP,
            redis=redis,
            namespace=EmailVerificationOTPCacheConfig.NAMESPACE.value,
            ttl=EmailVerificationOTPCacheConfig.TTL.value,
        )
