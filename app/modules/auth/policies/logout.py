from app.adapters.db.models.user import User
from ..commands.logout import LogoutCommand


class LogoutPolicy:
    async def __call__(self, actor: User | None, command: LogoutCommand) -> None:
        pass
