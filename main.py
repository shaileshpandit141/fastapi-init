from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import from_url

from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from core.settings import settings
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


# Create FastAPI app
app = FastAPI(title=settings.app_name, lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define root url to check health
@app.get("/", tags=["health"])
async def check_health() -> dict[str, str]:
    return {"status": "ok"}


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
