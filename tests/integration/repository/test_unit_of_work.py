import pytest

from core.repository import Repository
from core.repository.actions.create import AsyncSession, CreateAction
from core.repository.unit_of_work import UnitOfWork
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_unit_of_work_commit(async_session: AsyncSession) -> None:
    repo = Repository(async_session)

    async with UnitOfWork(repo) as uow:
        result = await uow.repo.execute(
            CreateAction(Role, [Role(name="boot")]),
        )

    # Committed automatically
    assert result[0].name == "boot"
