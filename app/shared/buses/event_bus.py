from typing import Any
from app.shared.protocols.event import Event


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Any]] = {}

    def register(self, event: type, handler: Any) -> None:
        self._handlers.setdefault(event, []).append(handler)

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            handlers = self._handlers.get(type(event), [])
            for handler in handlers:
                await handler(event)
