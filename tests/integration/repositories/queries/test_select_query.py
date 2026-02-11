import pytest

from core.repositoriesx.queries.select import AsyncSession, SelectQuery
from domain.role.models import Role


@pytest.mark.asyncio
@pytest.mark.integration
async def test_select_query(async_session: AsyncSession) -> None:
    roles = [Role(name="staff"), Role(name="guest")]

    async_session.add_all(roles)
    await async_session.commit()

    query = SelectQuery(Role, where=[Role.name == "staff"])
    result = await query.execute(async_session)

    # Assertions
    assert len(result) > 0
    assert result[0].name == "staff"
