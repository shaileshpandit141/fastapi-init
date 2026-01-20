# pyright: reportUnusedFunction=false

from asyncio import TimeoutError
from logging import getLogger

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from httpx import HTTPError
from jose import JWTError
from redis.exceptions import RedisError
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_504_GATEWAY_TIMEOUT,
)

from core.exceptions import AppHTTPException

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    # Http related exceptions (highest priority)
    @app.exception_handler(AppHTTPException)
    async def app_exception_handler(
        request: Request, exc: AppHTTPException
    ) -> JSONResponse:
        logger.debug(msg="App http exception error", exc_info=exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # Rate limit exceeded
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded(
        request: Request, exc: RateLimitExceeded
    ) -> JSONResponse:
        logger.debug(msg="Rate limit exceeded", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": "Rate limit exceeded"},
        )

    # Jose jwt exception
    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
        logger.debug(msg="Jose jwt error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Authentication failed"},
        )

    # Permission error
    @app.exception_handler(PermissionError)
    async def permission_error_handler(
        request: Request, exc: PermissionError
    ) -> JSONResponse:
        logger.debug(msg="Permission denied error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": "Access denied"},
        )

    # Validation errors (FastAPI / Pydantic)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.debug(msg="Validation error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(TimeoutError)
    async def timeout_error_handler(
        request: Request, exc: TimeoutError
    ) -> JSONResponse:
        logger.debug(msg="Request timeout error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "Request timeout"},
        )

    # Redis exception handler
    @app.exception_handler(RedisError)
    async def redis_error_handler(request: Request, exc: RedisError) -> JSONResponse:
        logger.debug(msg="Redis error", exc_info=exc)
        return JSONResponse(
            status_code=503,
            content={"detail": "Cache service unavailable"},
        )

    # Database integrity errors
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        logger.debug(msg="DB integrity error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": "Resource already exists"},
        )

    # Httpx exception handler
    @app.exception_handler(HTTPError)
    async def httpx_error_handler(request: Request, exc: HTTPError) -> JSONResponse:
        logger.debug(msg="Httpx error", exc_info=exc)
        return JSONResponse(
            status_code=HTTP_502_BAD_GATEWAY,
            content={"detail": "External service failed"},
        )

    # HTTPException (fallback for routers / deps)
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        logger.debug(msg="Http exception error", exc_info=exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # Catch-all (500)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
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
