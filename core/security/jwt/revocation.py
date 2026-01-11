from redis.asyncio.client import Redis

from ...utils.time import time


async def revoke_token(redis: Redis, jti: str, exp: int) -> None:
    ttl = max(exp - int(time.utc_now().timestamp()), 0)  # seconds until expiry
    if ttl > 0:
        await redis.set(f"blocklist:{jti}", "1", ex=ttl)


async def is_token_revoked(redis: Redis, jti: str) -> bool:
    if await redis.get(f"blocklist:{jti}"):
        return True
    return False
