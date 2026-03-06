from typing import Any, Callable

from app.adapters.db.models.user import User
from app.shared.protocols.command import Command
from app.shared.protocols.uow import UnitOfWork
from app.shared.protocols.handlers import CommandHandler, CommandPolicy
from .event_bus import EventBus


class CommandBus:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        event_bus: EventBus,
    ) -> None:
        self._policies: dict[type, Any] = {}
        self._handlers: dict[type, Any] = {}
        self._uow_factory = uow_factory
        self._event_bus = event_bus

    def register(
        self,
        command: type,
        *,
        policy: CommandPolicy,
        handler: CommandHandler,
    ) -> None:
        self._policies[command] = policy
        self._handlers[command] = handler

    async def dispatch(self, actor: User | None, command: Command) -> Any:
        policy = self._policies.get(type(command))
        handler = self._handlers.get(type(command))

        if not handler or not policy:
            raise ValueError(f"No handler for {type(command).__name__}")

        await policy(actor, command)

        async with self._uow_factory() as uow:
            result = await handler(command)
            await uow.session.flush()

            # Publish domain events AFTER commit
            await self._event_bus.publish(uow.events)

        return result
