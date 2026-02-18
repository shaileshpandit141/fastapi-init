from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseCommand

# =============================================================================
# Save Updated Model Instance
# =============================================================================


class Save[T: SQLModel](BaseCommand[T]):
    def __init__(self, obj: T) -> None:
        self.obj = obj

    async def execute(self, session: AsyncSession) -> T:
        session.add(self.obj)
        return self.obj
