from typing import Any, Mapping, Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseCommand

# =============================================================================
# Insert One Record
# =============================================================================


class InsertOne[T: SQLModel](BaseCommand[T]):
    def __init__(
        self,
        *,
        model: type[T],
        data: SQLModel | BaseModel,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        self.model = model
        self.data = data
        self.extra = extra or {}

    async def execute(self, session: AsyncSession) -> T:
        obj = self.model(**self.data.model_dump(), **self.extra)
        session.add(obj)
        return obj


# =============================================================================
# Insert Many Records
# =============================================================================


class InsertMany[T: SQLModel](BaseCommand[Sequence[T]]):
    def __init__(
        self,
        *,
        model: type[T],
        data: Sequence[SQLModel | BaseModel],
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        self.model = model
        self.data = data
        self.extra = extra or {}

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        objs = [self.model(**item.model_dump(), **self.extra) for item in self.data]
        session.add_all(objs)
        return objs
