from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis


RedisDep = Annotated[Redis, Depends(get_redis)]
