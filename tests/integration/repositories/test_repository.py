from typing import Sequence

import pytest

from core.repositoriesx import Repository
from core.repositoriesx.commands.create import AsyncSession, Create
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_repository_execute(async_session: AsyncSession) -> None:
    roles = [Role(name="unknown")]
    command = Create(Role, roles)

    repo = Repository[Sequence[Role]](async_session)

    result = await repo.execute(command)
    await async_session.commit()

    assert result[0].name == "unknown"
