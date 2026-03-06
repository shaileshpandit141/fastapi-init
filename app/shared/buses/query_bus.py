from typing import Any

from app.adapters.db.models.user import User
from app.shared.protocols.query import Query
from app.shared.protocols.handlers import QueryHandler, QueryPolicy


class QueryBus:
    def __init__(self) -> None:
        self._handlers: dict[type, Any] = {}
        self._policies: dict[type, Any] = {}

    def register(
        self,
        query: type,
        *,
        policy: QueryPolicy,
        handler: QueryHandler,
    ) -> None:
        self._policies[query] = policy
        self._handlers[query] = handler

    async def dispatch(self, actor: User | None, query: Query) -> Any:
        policy = self._policies.get(type(query))
        handler = self._handlers.get(type(query))

        if not handler or not policy:
            raise ValueError(f"No handler for {type(query).__name__}")

        await policy(actor, query)

        return await handler(query)
