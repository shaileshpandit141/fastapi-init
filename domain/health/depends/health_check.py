from typing import Annotated

from fastapi import Depends, Response

from core.db.depends import AsyncSessionDep
from infrastructure.cache.depends.redis import RedisDep

from ..services.health_check import HealthCheckService

# === Health Service Dep ===


async def get_health_service(
    redis: RedisDep, session: AsyncSessionDep, response: Response
) -> HealthCheckService:
    return HealthCheckService(redis=redis, session=session, response=response)


HealthCheckServiceDep = Annotated[HealthCheckService, Depends(get_health_service)]
