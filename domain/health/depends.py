from typing import Annotated

from fastapi import Depends, Response

from core.db.deps import AsyncSessionDep
from domain.health.service import HealthCheckService
from infrastructure.cache.redis import RedisDep

# === Health Service Dep ===


async def get_health_service(
    redis: RedisDep, session: AsyncSessionDep, response: Response
) -> HealthCheckService:
    return HealthCheckService(
        redis=redis,
        session=session,
        response=response,
    )


HealthCheckServiceDep = Annotated[HealthCheckService, Depends(get_health_service)]
