from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.auth.commands.login import LoginCommand
from app.shared.buses.command_bus import CommandBus
from ..dependencies import get_command_bus
from ..schemas.login import Login

router = APIRouter(prefix="/auth", tags=["Auth Endpoints"])

# =============================================================================
# User login endpoint.
# =============================================================================


@router.post(
    path="/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    bus: CommandBus = Depends(get_command_bus),
) -> Login:
    tokens = await bus.dispatch(
        actor=None,
        command=LoginCommand(
            email=form.username,
            password=form.password,
        ),
    )
    return Login(**tokens)
