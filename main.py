from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from redis.asyncio import from_url

from api.v1.auth import router as auth_router
from api.v1.health import router as health_router
from api.v1.users import router as users_router
from core.config import settings
from core.config.logging import LOGGING_CONFIG
from db.engine import engine, init_db


# Create a async lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.redis = from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    try:
        await init_db()
        yield
    finally:
        await app.state.redis.close()
        await engine.dispose()


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
