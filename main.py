from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from redis.exceptions import ConnectionError
from slowapi.errors import RateLimitExceeded

from api.router import api_router
from core.lifespan import lifespan
from core.logging import LOGGING_CONFIG
from core.middleware import include_middlewares
from core.settings import settings
from infrastructure.cache.redis.handlers.connection import redis_connection_handler
from infrastructure.limiter import limiter
from infrastructure.limiter.handler import rate_limit_handler


def create_app() -> FastAPI:

    # Configure logging
    dictConfig(LOGGING_CONFIG)

    # Creating a FastAPI app
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    # Add something to app state
    app.state.limiter = limiter

    # Add custom exception handler
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app.add_exception_handler(ConnectionError, redis_connection_handler)

    # Include all middlewares
    include_middlewares(app)

    # Define root url to redirect /docs page
    @app.get("/", include_in_schema=False)
    async def _() -> RedirectResponse:
        return RedirectResponse(url="/docs", status_code=307)

    # Include api routers
    app.include_router(api_router)

    # Return created app
    return app


# Create a fastapi app
app = create_app()
