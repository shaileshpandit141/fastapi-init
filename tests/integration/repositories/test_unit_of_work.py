from typing import Sequence

import pytest

from core.repositoriesx import Repository
from core.repositoriesx.commands.create import AsyncSession, Create
from core.repositoriesx.unit_of_work import UnitOfWork
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_unit_of_work_commit(async_session: AsyncSession) -> None:
    repo = Repository[Sequence[Role]](async_session)
    async with UnitOfWork[Sequence[Role]](repo) as uow:
        roles = [Role(name="boot")]
        command = Create(Role, roles)
        result = await uow.repo.execute(command)

    # Committed automatically
    assert result[0].name == "boot"
