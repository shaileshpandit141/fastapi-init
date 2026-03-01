from functools import lru_cache

from app.application.bus.command_bus import CommandBus
from app.application.bus.query_bus import QueryBus

# =============================================================================
# Get command bus dependency.
# =============================================================================


@lru_cache
def get_command_bus() -> CommandBus:
    bus = CommandBus()

    return bus


# =============================================================================
# Get query bus dependency.
# =============================================================================


@lru_cache
def get_query_bus() -> QueryBus:
    bus = QueryBus()

    return bus
