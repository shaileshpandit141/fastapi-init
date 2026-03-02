from pydantic import BaseModel

# =============================================================================
# Login User Related Schema.
# =============================================================================


class Login(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# =============================================================================
# Refresh Token Schema.
# =============================================================================


class RefreshToken(Login):
    pass
