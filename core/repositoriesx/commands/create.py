from typing import Any, Mapping, Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel

from ..commands import AsyncSession, RepoCommand

# =============================================================================
# Create Record Command
# =============================================================================


class Create[T: SQLModel, D: SQLModel | BaseModel](RepoCommand[list[T]]):
    def __init__(
        self,
        model: type[T],
        data: Sequence[D],
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        self.model = model
        self.data = data
        self.extra = extra or {}

    async def execute(self, session: AsyncSession) -> list[T]:
        objs = [self.model(**item.model_dump(), **self.extra) for item in self.data]
        session.add_all(objs)
        return objs
