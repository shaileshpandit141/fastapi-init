import json
from logging import getLogger
from typing import Any

from fastapi import APIRouter, Response, status
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from dependencies.cache.redis import RedisDep
from dependencies.connections.session import SessionDep
from schemas.health import HealthyRead, UnhealthyRead

router = APIRouter(prefix="/health", tags=["health"])

logger = getLogger(__name__)


HEALTH_CACHE_KEY = "health_status"
HEALTHY_TTL = 30  # seconds
UNHEALTHY_TTL = 5  # seconds


HEALTH_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {"model": HealthyRead, "description": "Service is healthy"},
    503: {"model": UnhealthyRead, "description": "Service is unhealthy"},
}


@router.get(
    "/",
    summary="Health check",
    response_model=HealthyRead | UnhealthyRead,
    responses=HEALTH_RESPONSES,
)
async def health_check(
    redis: RedisDep, session: SessionDep, response: Response
) -> HealthyRead | UnhealthyRead:
    # Try returning cached health
    cached_raw = await redis.get(HEALTH_CACHE_KEY)
    if cached_raw:
        cached_health = json.loads(cached_raw)
        logger.debug("Returning cached health status: %s", cached_health)

        if cached_health["status"] != "ok":
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return (
            HealthyRead(**cached_health)
            if cached_health["status"] == "ok"
            else UnhealthyRead(**cached_health)
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
        HealthyRead(**health_data)
        if health_status == "ok"
        else UnhealthyRead(**health_data)
    )
