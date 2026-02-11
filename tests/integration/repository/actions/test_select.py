import pytest

from core.repository.actions.select import AsyncSession, SelectAction
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_select_action(async_session: AsyncSession) -> None:
    roles = [Role(name="staff"), Role(name="guest")]

    async_session.add_all(roles)
    await async_session.commit()

    action = SelectAction(Role, where=[Role.name == "staff"])
    result = await action.execute(async_session)

    # Assertions
    assert len(result) > 0
    assert result[0].name == "staff"
