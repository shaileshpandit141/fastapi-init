import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from dependencies.redis import RedisDep
from dependencies.session import SessionDep

router = APIRouter(prefix="/healthz", tags=["health"])


HEALTH_CACHE_KEY = "system_health_status"
HEALTHY_TTL = 30  # seconds
UNHEALTHY_TTL = 5  # seconds


@router.get("/", summary="Health check")
async def check_health(
    redis: RedisDep,
    session: SessionDep,
) -> JSONResponse:
    cached_raw = await redis.get(HEALTH_CACHE_KEY)
    if cached_raw:
        if isinstance(cached_raw, (bytes, bytearray)):
            cached_health = json.loads(cached_raw.decode())
        elif isinstance(cached_raw, str):
            cached_health = json.loads(cached_raw)
        else:
            cached_health = cached_raw

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
        health_data["status"] = "unhealthy"

    ttl = HEALTHY_TTL if health_data["status"] == "ok" else UNHEALTHY_TTL
    await redis.set(HEALTH_CACHE_KEY, json.dumps(health_data), ex=ttl)

    return JSONResponse(
        content=health_data,
        status_code=(
            status.HTTP_200_OK
            if health_data["status"] == "ok"
            else status.HTTP_503_SERVICE_UNAVAILABLE
        ),
    )
