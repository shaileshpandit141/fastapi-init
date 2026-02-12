import pytest

from core.repository import Repository
from core.repository.actions.select import AsyncSession, SelectOne
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_repository_execute(async_session: AsyncSession) -> None:
    repo = Repository(async_session)
    role = await repo.execute(
        SelectOne(
            model=Role,
            where=[Role.name == "role-5"],
        )
    )
    await async_session.commit()

    # Assertion
    assert role.name == "role-5" # type: ignore
