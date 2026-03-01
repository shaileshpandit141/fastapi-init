from typing import Any, Protocol

# =============================================================================
# Actor protocol.
# =============================================================================


class Actor(Protocol): ...


# =============================================================================
# Command protocol.
# =============================================================================


class Command(Protocol): ...


# =============================================================================
# Command handler protocol.
# =============================================================================


class CommandHandler[C: Command, R](Protocol):
    async def __call__(self, command: C) -> R: ...


# =============================================================================
# Command policy protocol.
# =============================================================================


class CommandPolicy[C: Command, A: Actor](Protocol):
    async def __call__(self, command: C, actor: A) -> None: ...


# =============================================================================
# Command bus to handle all things.
# =============================================================================


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[type[Command], CommandHandler[Any, Any]] = {}
        self._policies: dict[type[Command], CommandPolicy[Any, Any]] = {}

    def register(
        self,
        command: type[Command],
        handler: CommandHandler[Any, Any],
        policy: CommandPolicy[Any, Any],
    ) -> None:
        self._handlers[command] = handler
        self._policies[command] = policy

    async def dispatch(self, command: Command, actor: Actor) -> Any:  # noqa: ANN401
        handler = self._handlers.get(type(command))
        if handler is None:
            msg = f"No handler registered for {type(command).__name__}"
            raise ValueError(msg)

        policy = self._policies.get(type(command))
        if policy is None:
            msg = f"No policy registered for {type(command).__name__}"
            raise ValueError(msg)

        await policy(command, actor)

        return await handler(command)
