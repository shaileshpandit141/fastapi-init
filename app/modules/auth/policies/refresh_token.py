from app.adapters.db.models.user import User
from ..commands.refresh_token import RefreshTokenCommand


class RefreshTokenPolicy:
    async def __call__(self, actor: User | None, command: RefreshTokenCommand) -> None:
        pass
