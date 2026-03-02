from typing import Any

from app.shared.protocols.actor import Actor
from app.shared.protocols.query import Query


class QueryBus:
    def __init__(self) -> None:
        self._handlers: dict[type, Any] = {}
        self._policies: dict[type, Any] = {}

    def register(self, query: type, handler: Any, policy: Any) -> None:
        self._handlers[query] = handler
        self._policies[query] = policy

    async def dispatch(self, query: Query, actor: Actor) -> Any:
        handler = self._handlers.get(type(query))
        policy = self._policies.get(type(query))

        if not handler or not policy:
            raise ValueError(f"No handler for {type(query).__name__}")

        await policy(query, actor)
        result = await handler(query)

        return result
