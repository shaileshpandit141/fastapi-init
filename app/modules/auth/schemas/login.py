from pydantic import BaseModel

# =============================================================================
# Login User Related Schema.
# =============================================================================


class UserLogin(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
