from collections.abc import AsyncGenerator

from .session import SessionLocal


async def get_session() -> AsyncGenerator:
    async with SessionLocal() as session:
        yield session
