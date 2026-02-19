from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from .config import get_settings

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()


# =============================================================================
# Function That Include All Middlewares.
# =============================================================================


def include_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.ALLOW_ORIGINS,
        allow_methods=settings.cors.ALLOW_METHODS,
        allow_headers=settings.cors.ALLOW_HEADERS,
        allow_credentials=settings.cors.ALLOW_CREDENTIALS,
    )
    app.add_middleware(SlowAPIMiddleware)
