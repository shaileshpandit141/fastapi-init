from pydantic import BaseModel

# =============================================================================
# TokenRead User Related Schema.
# =============================================================================


class TokenRead(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
