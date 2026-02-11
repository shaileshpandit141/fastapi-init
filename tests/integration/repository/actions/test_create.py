import pytest

from core.repository.actions.insert import AsyncSession, InsertMany
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_action(async_session: AsyncSession) -> None:
    action = InsertMany(model=Role, data=[Role(name="admin")])
    result = await action.execute(async_session)
    await async_session.commit()

    # Assertions
    assert len(result) == 1
    assert result[0].name == "admin"
