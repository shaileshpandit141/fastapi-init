from pydantic import BaseModel

# =============================================================================
# Refresh token Schema.
# =============================================================================


class RefreshToken(BaseModel):
    refresh_token: str
