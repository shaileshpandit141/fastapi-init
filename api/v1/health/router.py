import json
from logging import getLogger
from typing import Any

from fastapi import APIRouter, Response, status
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from dependencies.redis import RedisDep
from dependencies.session import SessionDep
from schemas.health import HealthyResponse, UnhealthyResponse

router = APIRouter(prefix="/health", tags=["health"])

logger = getLogger(__name__)


HEALTH_CACHE_KEY = "health_status"
HEALTHY_TTL = 30  # seconds
UNHEALTHY_TTL = 5  # seconds


HEALTH_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {"model": HealthyResponse, "description": "Service is healthy"},
    503: {"model": UnhealthyResponse, "description": "Service is unhealthy"},
}


@router.get(
    "/",
    summary="Health check",
    response_model=HealthyResponse | UnhealthyResponse,
    responses=HEALTH_RESPONSES,
)
async def health_check(
    redis: RedisDep, session: SessionDep, response: Response
) -> HealthyResponse | UnhealthyResponse:
    # Try returning cached health
    cached_raw = await redis.get(HEALTH_CACHE_KEY)
    if cached_raw:
        cached_health = json.loads(cached_raw)
        logger.debug("Returning cached health status: %s", cached_health)

        if cached_health["status"] != "ok":
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return (
            HealthyResponse(**cached_health)
            if cached_health["status"] == "ok"
            else UnhealthyResponse(**cached_health)
        )

    # Compute health
    health_status = "ok"

    try:
        await session.exec(select(1))
    except OperationalError:
        logger.exception("Database health check failed")
        health_status = "unhealthy"

    # Cache the result
    ttl = HEALTHY_TTL if health_status == "ok" else UNHEALTHY_TTL
    health_data = {"status": health_status}
    await redis.set(HEALTH_CACHE_KEY, json.dumps(health_data), ex=ttl)

    logger.debug("Returning new health status: %s", health_data)

    if health_status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return (
        HealthyResponse(**health_data)
        if health_status == "ok"
        else UnhealthyResponse(**health_data)
    )
