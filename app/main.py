from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from .api.router import router
from .core.config import get_settings
from .core.exc_handlers import register_exception_handlers
from .core.lifespan import lifespan
from .core.logging import LOGGING_CONFIG
from .core.middleware import include_middlewares
from .infrastructure.rate_limit.limiter import limiter

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
