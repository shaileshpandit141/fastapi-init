# pyright: reportArgumentType=false

from logging import getLogger
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import JWTError
from redis.exceptions import RedisError
from slowapi.errors import RateLimitExceeded
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from .exceptions._base import AppError
from .exceptions.http import HttpError

# =============================================================================
# Getting logger for this file.
# =============================================================================


logger = getLogger(__name__)

# =============================================================================
# App Http level exceptions.
# =============================================================================


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.debug(msg="App error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


# =============================================================================
# App Http level exceptions.
# =============================================================================


async def app_http_error_handler(request: Request, exc: HttpError) -> JSONResponse:
    logger.debug(msg="App http error", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# =============================================================================
# Rate Limit Exceeded.
# =============================================================================


def rate_limit_exceeded(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.debug(msg="Rate limit exceeded", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"},
    )


# =============================================================================
# Jose Jwt Exception.
# =============================================================================


async def jose_jwt_error_handler(request: Request, exc: JWTError) -> JSONResponse:
    logger.debug(msg="Jose jwt error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Authentication failed"},
    )


# =============================================================================
# Redis Exception Handler.
# =============================================================================


async def redis_error_handler(request: Request, exc: RedisError) -> JSONResponse:
    logger.debug(msg="Redis error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Cache service unavailable"},
    )


# =============================================================================
# Catch-all (500).
# =============================================================================


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.debug(
        msg="Unhandled exception",
        exc_info=exc,
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )


# =============================================================================
# List of All Exception Handlers.
# =============================================================================


error_handlers: list[tuple[Any, Any]] = [
    (AppError, app_error_handler),
    (HttpError, app_http_error_handler),
    (RateLimitExceeded, rate_limit_exceeded),
    (JWTError, jose_jwt_error_handler),
    (RedisError, redis_error_handler),
    (Exception, unhandled_error_handler),
]


# =============================================================================
# Function to Register All Exception Handlers.
# =============================================================================


def register_exception_handlers(app: FastAPI) -> None:
    for error_handler in error_handlers:
        app.add_exception_handler(error_handler[0], error_handler[1])
