from pydantic import BaseModel
from redis.asyncio import Redis

from ..constants.user import USER_CACHE_TTL


class UserCache:

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @staticmethod
    def _key(user_id: int | str) -> str:
        return f"user:auth:{user_id}"

    async def get(
        self, user_id: int | str, schema: type[BaseModel]
    ) -> BaseModel | None:
        """Get cached snapshot"""

        data = await self.redis.get(self._key(user_id))
        if not data:
            return None

        return schema.model_validate_json(data)

    async def set(
        self, user_id: int | str, payload: BaseModel, ttl: int = USER_CACHE_TTL
    ) -> None:
        """Cache provided snapshot"""

        await self.redis.setex(self._key(user_id), ttl, payload.model_dump_json())

    async def invalidate(self, user_id: int | str) -> None:
        """Invalidate cached snapshot"""

        await self.redis.delete(self._key(user_id))

    async def exists(self, user_id: int | str) -> bool:
        return bool(await self.redis.exists(self._key(user_id)))
