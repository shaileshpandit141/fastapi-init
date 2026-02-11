import pytest

from core.repository import Repository
from core.repository.actions.insert import AsyncSession, InsertMany
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_repository_execute(async_session: AsyncSession) -> None:
    repo = Repository(async_session)
    result = await repo.execute(
        InsertMany(
            model=Role,
            data=[Role(name="something")],
        )
    )
    await async_session.commit()

    assert result[0].name == "something"
