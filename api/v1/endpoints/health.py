from fastapi import APIRouter

from domain.health.deps import HealthCheckServiceDep
from domain.health.schemas import HealthyRead, UnhealthyRead
from domain.response.schemas import OpenAPIResponses

router = APIRouter(prefix="/health", tags=["Health Endpoints"])


OPEN_API_RESPONSES: OpenAPIResponses = {
    200: {"model": HealthyRead, "description": "Service is healthy"},
    503: {"model": UnhealthyRead, "description": "Service is unhealthy"},
}


@router.get(
    "/",
    summary="Health check",
    description="Check server health by calling the endpoint",
    response_model=HealthyRead | UnhealthyRead,
    responses=OPEN_API_RESPONSES,
)
async def health_check(
    health_service: HealthCheckServiceDep,
) -> HealthyRead | UnhealthyRead:
    return await health_service.health_check()
