from typing import Any

from fastapi import APIRouter

from domain.health.deps import HealthCheckServiceDep
from domain.health.schemas import HealthyRead, UnhealthyRead

router = APIRouter(prefix="/health", tags=["Health Endpoints"])


HEALTH_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {"model": HealthyRead, "description": "Service is healthy"},
    503: {"model": UnhealthyRead, "description": "Service is unhealthy"},
}


@router.get(
    "/",
    summary="Health check",
    description="Check server health by calling the endpoint",
    response_model=HealthyRead | UnhealthyRead,
    responses=HEALTH_RESPONSES,
)
async def health_check(
    health_service: HealthCheckServiceDep,
) -> HealthyRead | UnhealthyRead:
    return await health_service.health_check()
