# pyright: reportArgumentType=false

from logging import getLogger
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError
from redis.exceptions import RedisError
from slowapi.errors import RateLimitExceeded
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from core.exceptions import AppHTTPException

logger = getLogger(__name__)

# === App exceptions (highest priority) ===


async def app_exception_handler(
    request: Request, exc: AppHTTPException
) -> JSONResponse:
    logger.debug(msg="App http exception error", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# === Rate limit exceeded ===


def rate_limit_exceeded(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.debug(msg="Rate limit exceeded", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_409_CONFLICT,
        content={"detail": "Rate limit exceeded"},
    )


# === Jose jwt exception ===


def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
    logger.debug(msg="Jose jwt error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Authentication failed"},
    )


# === Permission error ===


def permission_denie_handler(request: Request, exc: PermissionError) -> JSONResponse:
    logger.debug(msg="Permission denied error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_403_FORBIDDEN,
        content={"detail": "Access denied"},
    )


# === Validation errors (FastAPI / Pydantic) ===


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.debug(msg="Validation error", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


# === Redis exception handler ===


def redis_exception_handler(request: Request, exc: RedisError) -> JSONResponse:
    logger.debug(msg="Redis error", exc_info=exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "Cache service unavailable"},
    )


# === HTTPException (fallback for routers / deps) ===


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.debug(msg="Http exception error", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# === Catch-all (500) ===


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
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
        content={"detail": "Something went wrong"},
    )


# === List of all exception handlers ===


exception_handler_list: list[tuple[Any, Any]] = [
    (AppHTTPException, app_exception_handler),
    (RateLimitExceeded, rate_limit_exceeded),
    (JWTError, jwt_exception_handler),
    (PermissionError, permission_denie_handler),
    (RequestValidationError, validation_exception_handler),
    (RedisError, redis_exception_handler),
    (HTTPException, http_exception_handler),
    (Exception, unhandled_exception_handler),
]


# === Define a function to register all exception handlers ===


def register_exception_handlers(app: FastAPI) -> None:
    for exc_handler in exception_handler_list:
        app.add_exception_handler(exc_handler[0], exc_handler[1])
