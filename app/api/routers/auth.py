from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.auth.commands.login import LoginCommand
from app.modules.auth.commands.logout import LogoutCommand
from app.modules.auth.commands.refresh_token import RefreshTokenCommand
from app.shared.buses.command_bus import CommandBus
from app.shared.response.schemas import DetailResponse

from ..dependencies import get_command_bus
from ..schemas.login import TokenRead
from ..schemas.logout import Logout
from ..schemas.refresh_token import RefreshToken

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
) -> TokenRead:
    tokens = await bus.dispatch(
        actor=None,
        command=LoginCommand(
            email=form.username,
            password=form.password,
        ),
    )
    return TokenRead(**tokens)


# =============================================================================
# Token refresh endpoint.
# =============================================================================


@router.post(
    path="/refresh",
    summary="Refresh access token",
    description="Refresh access token using a valid refresh token.",
)
async def refresh_token(
    payload: RefreshToken,
    bus: CommandBus = Depends(get_command_bus),
) -> TokenRead:
    tokens = await bus.dispatch(
        actor=None,
        command=RefreshTokenCommand(
            refresh_token=payload.refresh_token,
        ),
    )
    return TokenRead(**tokens)


# =============================================================================
# User logout endpoint.
# =============================================================================


@router.post(
    path="/logout",
    summary="Logout authenticated user",
    description="Blacklist access and refresh token.",
)
async def logout(
    payload: Logout,
    bus: CommandBus = Depends(get_command_bus),
) -> DetailResponse:
    message = await bus.dispatch(
        actor=None,
        command=LogoutCommand(
            refresh_token=payload.refresh_token,
            access_token=payload.access_token,
        ),
    )
    return DetailResponse(**message)
