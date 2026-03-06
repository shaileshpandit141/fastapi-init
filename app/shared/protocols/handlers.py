from typing import Any, Protocol
from redis.asyncio import Redis
from sqlmodel.ext.asyncio.session import AsyncSession


# =============================================================================
# Command Handler Protocol
# =============================================================================


class CommandHandler(Protocol):
    redis: Redis
    session: AsyncSession

    async def __call__(self, command: Any) -> Any: ...


# =============================================================================
# Query Handler Protocol.
# =============================================================================


class QueryHandler(Protocol):
    redis: Redis
    session: AsyncSession

    async def __call__(self, query: Any) -> Any: ...


# =============================================================================
# Command Policy Protocol.
# =============================================================================


class CommandPolicy(Protocol):
    async def __call__(self, actor: Any, command: Any) -> None:
        pass


class QueryPolicy(Protocol):
    async def __call__(self, actor: Any, query: Any) -> None:
        pass
