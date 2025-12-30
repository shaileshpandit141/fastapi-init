from redis.asyncio.client import Redis

from utils.get_utc_now import get_utc_now


async def revoke_token(redis: Redis, jti: str, exp: int) -> None:
    ttl = max(exp - int(get_utc_now().timestamp()), 0)  # seconds until expiry
    await redis.set(f"blocklist:{jti}", "1", ex=ttl)


async def is_token_revoked(redis: Redis, jti: str) -> bool:
    if await redis.get(f"blocklist:{jti}"):
        return True
    return False
