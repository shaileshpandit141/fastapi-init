from pydantic import BaseModel, EmailStr

# =============================================================================
# Register User Related Schema.
# =============================================================================


class RegisterUser(BaseModel):
    email: EmailStr
    password: str
