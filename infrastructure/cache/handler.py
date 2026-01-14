from fastapi import Request
from fastapi.responses import JSONResponse


def redis_connection_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "code": "REDIS_CONNECTION_ERROR",
            "message": "Service temporarily unavailable",
            "debug": {"exception_args": exc.args},
        },
    )
