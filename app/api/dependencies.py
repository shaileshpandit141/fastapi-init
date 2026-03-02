from functools import lru_cache
from typing import Annotated
from redis.asyncio.client import Redis
from fastapi import Depends

from app.adapters.db.session import get_async_session
from app.adapters.db.unit_of_work import AsyncSession, AsyncUnitOfWork
from app.adapters.redis.client import get_async_redis
from app.shared.buses.command_bus import CommandBus
from app.shared.buses.event_bus import EventBus
from app.shared.buses.query_bus import QueryBus

from app.application.auth.commands.login import LoginCommand
from app.application.auth.commands.handlers.login import LoginCommandHandler
from app.application.auth.policies.login import LoginPolicy

# =============================================================================
# Getting event instance for dependency.
# =============================================================================


def get_event_bus() -> EventBus:
    bus = EventBus()
    return bus


# =============================================================================
# Getting command bus instance for dependency.
# =============================================================================


@lru_cache
def get_command_bus(
    redis: Annotated[Redis, Depends(get_async_redis)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
) -> CommandBus:
    bus = CommandBus(
        uow_factory=lambda: AsyncUnitOfWork(session),
        event_bus=event_bus,
    )

    bus.register(
        LoginCommand,
        LoginCommandHandler(redis, session),
        LoginPolicy(),
    )

    return bus


# =============================================================================
# Getting query bus for dependency.
# =============================================================================


@lru_cache
def get_query_bus(
    redis: Annotated[Redis, Depends(get_async_redis)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> QueryBus:
    bus = QueryBus()
    return bus
