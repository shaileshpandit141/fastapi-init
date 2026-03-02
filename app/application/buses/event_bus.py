from typing import Any, Protocol


# =============================================================================
# Event protocol.
# =============================================================================

class Event(Protocol): ...


# =============================================================================
# Event handler protocol.
# =============================================================================


class EventHandler[E: Event](Protocol):
    async def __call__(self, event: E) -> None: ...

# =============================================================================
# Event bus to handle all action.
# =============================================================================

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler[Any]]] = {}

    def register(self, event: type[Event], handler: EventHandler[Any]) -> None:
        self._handlers.setdefault(event, []).append(handler)

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            handlers = self._handlers.get(type(event), [])
            for handler in handlers:
                await handler(event)
