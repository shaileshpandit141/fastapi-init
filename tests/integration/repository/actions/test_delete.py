import pytest

from core.repository.actions.delete import AsyncSession, DeleteMany
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_action(async_session: AsyncSession) -> None:
    role = Role(name="manager")
    async_session.add(role)
    await async_session.commit()

    action = DeleteMany(objs=[role])
    deleted_count = await action.execute(async_session)
    await async_session.commit()

    # Assertions
    assert deleted_count == 1
