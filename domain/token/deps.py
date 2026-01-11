from typing import Annotated

from fastapi import Depends

from infrastructure.cache.redis import RedisDep

from .service import JwtTokenService


async def get_jwt_token_service(redis: RedisDep) -> JwtTokenService:
    return JwtTokenService(redis=redis)


JwtTokenServiceDep = Annotated[JwtTokenService, Depends(get_jwt_token_service)]
