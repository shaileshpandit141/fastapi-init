from sqlalchemy.engine import ScalarResult
from sqlmodel import SQLModel
from sqlmodel.sql.expression import SelectOfScalar

from .base import AsyncSession, BaseRepoAction

# =============================================================================
# Exexute Any Scalar Query Action
# =============================================================================


class ScalarQuery[T: SQLModel](BaseRepoAction[ScalarResult[T]]):
    def __init__(self, stmt: SelectOfScalar[T]) -> None:
        self.stmt = stmt

    async def execute(self, session: AsyncSession) -> ScalarResult[T]:
        result = await session.exec(self.stmt)
        return result
