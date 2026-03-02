from app.adapters.db.models.user import User
from ..commands.login import LoginCommand


class LoginPolicy:
    async def __call__(self, command: LoginCommand, actor: User | None) -> None:
        pass
