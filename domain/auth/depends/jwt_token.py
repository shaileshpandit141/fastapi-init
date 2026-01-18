from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from infrastructure.cache.depends.redis import RedisDep

from ..services.jwt_token import JwtTokenService

# === Jwt Token Service Dep ===


async def get_jwt_token_service(
    session: AsyncSessionDep, redis: RedisDep
) -> JwtTokenService:
    return JwtTokenService(session=session, redis=redis)


JwtTokenServiceDep = Annotated[JwtTokenService, Depends(get_jwt_token_service)]
