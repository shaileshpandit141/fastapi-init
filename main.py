from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.v1.auth import router as auth_router
from api.v1.health import router as health_router
from api.v1.users import router as users_router
from context.lifespan import lifespan
from core.config.logging import LOGGING_CONFIG
from core.config.settings import settings

# Configure logging
dictConfig(LOGGING_CONFIG)


# Create FastAPI app
app = FastAPI(title=settings.app_name, lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define root url to redirect /docs page
@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


# Include routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
