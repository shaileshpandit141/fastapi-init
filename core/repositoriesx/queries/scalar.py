from sqlalchemy.engine import ScalarResult
from sqlmodel import SQLModel
from sqlmodel.sql.expression import SelectOfScalar

from ..queries import AsyncSession, RepoQuery

# =============================================================================
# Exexute Any Scalar Query
# =============================================================================


class ScalarQuery[T: SQLModel](RepoQuery[ScalarResult[T]]):
    def __init__(self, stmt: SelectOfScalar[T]) -> None:
        self.stmt = stmt

    async def execute(self, session: AsyncSession) -> ScalarResult[T]:
        result = await session.exec(self.stmt)
        return result
