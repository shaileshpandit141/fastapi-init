from typing import Any, Callable

from app.shared.protocols.actor import Actor
from app.shared.protocols.command import Command
from app.shared.protocols.uow import UnitOfWork

from .event_bus import EventBus


class CommandBus:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        event_bus: EventBus,
    ) -> None:
        self._handlers: dict[type, Any] = {}
        self._policies: dict[type, Any] = {}
        self._uow_factory = uow_factory
        self._event_bus = event_bus

    def register(self, command: type, handler: Any, policy: Any) -> None:
        self._handlers[command] = handler
        self._policies[command] = policy

    async def dispatch(self, command: Command, actor: Actor) -> Any:
        handler = self._handlers.get(type(command))
        policy = self._policies.get(type(command))

        if not handler or not policy:
            raise ValueError(f"No handler for {type(command).__name__}")

        await policy(command, actor)

        async with self._uow_factory() as uow:
            result = await handler(command, uow)
            await uow.commit()

            # Publish domain events AFTER commit
            await self._event_bus.publish(uow.events)

        return result
