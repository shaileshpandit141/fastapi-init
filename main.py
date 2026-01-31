from logging.config import dictConfig
from typing import Callable

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.router import api_router
from core.handlers import register_exception_handlers
from core.lifespan import lifespan
from core.logging import LOGGING_CONFIG
from core.middleware import include_middlewares
from core.settings import settings
from infrastructure.rate_limit.limiter import limiter

# === A Root function to redirect user to /docs endpoint ===


def root_endpoint(app: FastAPI) -> Callable[[], RedirectResponse]:

    @app.get(path="/", include_in_schema=False)
    def _() -> RedirectResponse:
        return RedirectResponse(url="/docs", status_code=307)

    return _


# === Main function to create a fastapi app ===


def create_app() -> FastAPI:

    # Configure logging
    dictConfig(LOGGING_CONFIG)

    # Creating a FastAPI app
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    # Add something to app state
    app.state.limiter = limiter

    # Handle custom exception handler
    register_exception_handlers(app)

    # Include all middlewares
    include_middlewares(app)

    # Define root url to redirect /docs page
    root_endpoint(app)

    # Include api routers
    app.include_router(api_router)

    # Return created app
    return app


# === Create a fastapi app ===

app = create_app()
