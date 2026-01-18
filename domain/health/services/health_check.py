import json
from logging import getLogger

from fastapi import Response, status
from redis.asyncio.client import Redis
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from core.db.imports import AsyncSession

from ..constants.health_check import (
    HEALTH_CACHE_KEY,
    HEALTHY_TTL_SECONDS,
    UNHEALTHY_TTL_SECONDS,
)
from ..schemas.health_check import HealthyRead, UnhealthyRead

logger = getLogger(__name__)

# === Health Check Service ===


class HealthCheckService:
    def __init__(self, redis: Redis, session: AsyncSession, response: Response) -> None:
        self.redis = redis
        self.session = session
        self.response = response

    async def health_check(self) -> HealthyRead | UnhealthyRead:
        cached_raw = await self.redis.get(HEALTH_CACHE_KEY)
        if cached_raw:
            cached_health = json.loads(cached_raw)
            logger.debug("Returning cached health status: %s", cached_health)

            if cached_health["status"] != "ok":
                self.response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

            return (
                HealthyRead(**cached_health)
                if cached_health["status"] == "ok"
                else UnhealthyRead(**cached_health)
            )

        # Compute health
        health_status = "ok"

        try:
            await self.session.exec(select(1))
        except OperationalError:
            logger.exception("Database health check failed")
            health_status = "unhealthy"

        # Cache the result
        ttl = HEALTHY_TTL_SECONDS if health_status == "ok" else UNHEALTHY_TTL_SECONDS
        health_data = {"status": health_status}
        await self.redis.set(HEALTH_CACHE_KEY, json.dumps(health_data), ex=ttl)

        logger.debug("Returning new health status: %s", health_data)

        if health_status != "ok":
            self.response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return (
            HealthyRead(**health_data)
            if health_status == "ok"
            else UnhealthyRead(**health_data)
        )
