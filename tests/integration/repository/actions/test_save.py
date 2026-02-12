import pytest

from core.repository.actions.save import Save
from core.repository.actions.select import AsyncSession, SelectOne
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_select_one_action(async_session: AsyncSession) -> None:
    action = SelectOne(model=Role, where=[Role.name == "role-1"])
    role = await action.execute(async_session)

    if role is None:
        return None

    description = "update role description"
    role.description = description

    save_action = Save(role)
    updated_role = await save_action.execute(async_session)

    # Assertion
    assert updated_role.description == description
