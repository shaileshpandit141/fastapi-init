from fastapi import APIRouter, Depends

from app.adapters.db.models.user import User
from app.modules.user.queries.list import ListUserQuery
from app.shared.buses.query_bus import QueryBus
from app.shared.dependencies.get_current_user import get_current_user

from ..dependencies import get_query_bus
from ..schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["User Endpoints"])

# =============================================================================
# User endpoint.
# =============================================================================


@router.get(
    path="",
    summary="List users",
    description="List users only access by admin.",
)
async def list_user(
    limit: int = 20,
    offset: int = 0,
    actor: User = Depends(get_current_user),
    bus: QueryBus = Depends(get_query_bus),
) -> list[UserRead]:
    users = await bus.dispatch(
        actor=actor,
        query=ListUserQuery(
            limit=limit,
            offset=offset,
        ),
    )
    return users
