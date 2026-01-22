from typing import Annotated

from fastapi import Depends, Response

from core.db.depends.async_session import AsyncSessionDep
from infrastructure.cache.depends.redis import RedisDep

from .services import HealthCheckService

# === Health Service Dep ===


async def get_health_service(
    redis: RedisDep, session: AsyncSessionDep, response: Response
) -> HealthCheckService:
    return HealthCheckService(redis=redis, session=session, response=response)


HealthCheckServiceDep = Annotated[HealthCheckService, Depends(get_health_service)]
