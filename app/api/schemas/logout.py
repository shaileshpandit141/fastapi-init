from pydantic import BaseModel

# =============================================================================
# Logout User Related Schema.
# =============================================================================


class Logout(BaseModel):
    access_token: str
    refresh_token: str
