from typing import Any, Iterable, Sequence

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Mapper, selectinload
from sqlmodel import SQLModel, select

from .base import AsyncSession, BaseRepoAction

# =============================================================================
# List Relations Record Action
# =============================================================================


class ListWithRelations[T: SQLModel](BaseRepoAction[Sequence[T]]):
    def __init__(
        self,
        model: type[T],
        relations: Iterable[str],
        *,
        limit: int | None = None,
    ) -> None:
        self.model = model
        self.relations = relations
        self.limit = limit

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        stmt = select(self.model)

        mapper: Mapper[Any] = inspect(self.model)
        relationships = mapper.relationships.keys()

        for rel in self.relations:
            if rel not in relationships:
                raise ValueError(
                    f"{rel!r} is not a relationship on {self.model.__name__}"
                )
            stmt = stmt.options(selectinload(getattr(self.model, rel)))

        if self.limit:
            stmt = stmt.limit(self.limit)

        return (await session.exec(stmt)).all()
