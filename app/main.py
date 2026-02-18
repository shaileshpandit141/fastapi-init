from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from .api.router import router
from .infrastructure.rate_limit.limiter import limiter
from .shared.config import get_settings
from .shared.exc_handlers import register_exception_handlers
from .shared.lifespan import lifespan
from .shared.logging import LOGGING_CONFIG
from .shared.middleware import include_middlewares

# from app.infrastructure.rate_limit.constants import RateLimits
# from app.infrastructure.rate_limit.decorator import rate_limit


# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Setup Local Logger.
# =============================================================================

dictConfig(LOGGING_CONFIG)

# =============================================================================
# Creating FastAPI App Instance.
# =============================================================================

app = FastAPI(
    title=settings.app.NAME,
    debug=settings.app.DEBUG,
    lifespan=lifespan,
)

# =============================================================================
# Adding Slowapi limiter to FastAPI State.
# =============================================================================

app.state.limiter = limiter

# =============================================================================
# Register Custom Exception Handlers.
# =============================================================================

register_exception_handlers(app)

# =============================================================================
# Include All Middlewares.
# =============================================================================

include_middlewares(app)

# =============================================================================
# Redirect / Request to /docs Endpoint.
# =============================================================================


@app.get(path="/", include_in_schema=False)
def root(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


# =============================================================================
# Include Children routers.
# =============================================================================

app.include_router(router)
