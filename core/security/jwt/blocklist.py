from redis.asyncio.client import Redis

from core.utils.time import time

from .constants import BLOCKLIST_PREFIX


class JwtBlocklist:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def revoke(self, *, jti: str, exp: int) -> None:
        ttl = max(exp - int(time.utc_now().timestamp()), 0)
        if ttl > 0:
            await self.redis.set(f"{BLOCKLIST_PREFIX}{jti}", "1", ex=ttl)

    async def is_revoked(self, *, jti: str) -> bool:
        return bool(await self.redis.get(f"{BLOCKLIST_PREFIX}{jti}"))
