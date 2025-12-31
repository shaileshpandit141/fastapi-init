import json
from logging import getLogger

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from dependencies.redis import RedisDep
from dependencies.session import SessionDep

router = APIRouter(prefix="/health", tags=["health"])

logger = getLogger(__name__)

HEALTH_CACHE_KEY = "system_health_status"
HEALTHY_TTL = 30  # seconds
UNHEALTHY_TTL = 5  # seconds


@router.get("/", summary="Health check")
async def health_check(redis: RedisDep, session: SessionDep) -> JSONResponse:
    cached_raw = await redis.get(HEALTH_CACHE_KEY)

    if cached_raw:
        cached_health = json.loads(cached_raw)

        logger.debug("Returning cached health status: %s", cached_health)
        return JSONResponse(
            content=cached_health,
            status_code=(
                status.HTTP_200_OK
                if cached_health["status"] == "ok"
                else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )

    health_data = {"status": "ok"}

    try:
        await session.exec(select(1))
    except OperationalError:
        logger.exception("Database health check failed")
        health_data["status"] = "unhealthy"

    ttl = HEALTHY_TTL if health_data["status"] == "ok" else UNHEALTHY_TTL
    await redis.set(HEALTH_CACHE_KEY, json.dumps(health_data), ex=ttl)

    logger.debug("Returning new health status: %s", health_data)
    return JSONResponse(
        content=health_data,
        status_code=(
            status.HTTP_200_OK
            if health_data["status"] == "ok"
            else status.HTTP_503_SERVICE_UNAVAILABLE
        ),
    )
