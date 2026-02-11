import pytest

from core.repository.actions.create import AsyncSession, CreateAction
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_action(async_session: AsyncSession) -> None:
    action = CreateAction(Role, [Role(name="admin")])
    result = await action.execute(async_session)
    await async_session.commit()

    # Assertions
    assert len(result) == 1
    assert result[0].name == "admin"
