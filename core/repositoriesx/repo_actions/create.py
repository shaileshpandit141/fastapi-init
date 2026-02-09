from typing import Any, Mapping, Sequence

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

from ..exceptions import EntityConflictError
from .base import AsyncSession, BaseRepoAction

# =============================================================================
# Create One Record Action
# =============================================================================


class CreateOne[T: SQLModel, D: SQLModel | BaseModel](BaseRepoAction[T]):
    def __init__(
        self,
        model: type[T],
        data: D,
        extra: Mapping[str, Any] | None = None,
        *,
        refresh: bool = True,
    ) -> None:
        self.model = model
        self.data = data
        self.extra = extra or {}
        self.refresh = refresh

    async def execute(self, session: AsyncSession) -> T:
        try:
            obj = self.model(**self.data.model_dump(), **self.extra)
            session.add(obj)
            await session.commit()

            if self.refresh:
                await session.refresh(obj)

            return obj
        except IntegrityError:
            await session.rollback()
            raise EntityConflictError("Resource already exists")


# =============================================================================
# Create Many Records Action
# =============================================================================


class CreateMany[T: SQLModel, D: Sequence[SQLModel | BaseModel]](
    BaseRepoAction[Sequence[T]]
):
    def __init__(
        self,
        model: type[T],
        data: D,
        extra: Mapping[str, Any] | None = None,
        *,
        refresh: bool = False,
    ) -> None:
        self.model = model
        self.data = data
        self.extra = extra or {}
        self.refresh = refresh

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        objs = [self.model(**item.model_dump(), **self.extra) for item in self.data]

        session.add_all(objs)
        await session.commit()

        if self.refresh:
            for obj in objs:
                await session.refresh(obj)

        return objs
