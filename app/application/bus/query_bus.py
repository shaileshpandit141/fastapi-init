from typing import Any, Protocol

# =============================================================================
# Actor protocol.
# =============================================================================


class Actor(Protocol): ...


# =============================================================================
# Query protocol.
# =============================================================================


class Query(Protocol): ...


# =============================================================================
# Query handler protocol.
# =============================================================================


class QueryHandler[C: Query, R](Protocol):
    async def __call__(self, query: C) -> R: ...


# =============================================================================
# Query policy protocol.
# =============================================================================


class QueryPolicy[C: Query, A: Actor](Protocol):
    async def __call__(self, query: C, actor: A) -> None: ...


# =============================================================================
# Query bus to handle all things.
# =============================================================================


class QueryBus:
    def __init__(self) -> None:
        self._handlers: dict[type[Query], QueryHandler[Any, Any]] = {}
        self._policies: dict[type[Query], QueryPolicy[Any, Any]] = {}

    def register(
        self,
        query: type[Query],
        handler: QueryHandler[Any, Any],
        policy: QueryPolicy[Any, Any],
    ) -> None:
        self._handlers[query] = handler
        self._policies[query] = policy

    async def dispatch(self, query: Query, actor: Actor) -> Any:  # noqa: ANN401
        handler = self._handlers.get(type(query))
        if handler is None:
            msg = f"No handler registered for {type(query).__name__}"
            raise ValueError(msg)

        policy = self._policies.get(type(query))
        if policy is None:
            msg = f"No policy registered for {type(query).__name__}"
            raise ValueError(msg)

        await policy(query, actor)

        return await handler(query)
