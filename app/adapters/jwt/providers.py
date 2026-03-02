from redis.asyncio.client import Redis

from .manager import JwtTokenManager

# =============================================================================
# Function that return JwtTokenManager instance.
# =============================================================================


def get_jwt_token_manager(redis: Redis) -> JwtTokenManager:
    return JwtTokenManager(redis)
