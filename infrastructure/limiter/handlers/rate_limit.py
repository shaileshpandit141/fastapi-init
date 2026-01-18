from fastapi import Request
from fastapi.responses import JSONResponse


def rate_limit_handler(request: Request, exc: Exception) -> JSONResponse:

    return JSONResponse(
        status_code=429,
        content={
            "code": "RATE_LIMIT_EXCEEDED",
            "detail": getattr(exc, "detail", "Rate limit exceeded"),
            "debug": {"exception_args": exc.args},
        },
    )
