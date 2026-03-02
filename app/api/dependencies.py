from functools import lru_cache

from app.application.buses.command_bus import CommandBus
from app.application.buses.query_bus import QueryBus

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
