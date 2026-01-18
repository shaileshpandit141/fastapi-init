from fastapi.security import OAuth2PasswordBearer

# === OAuth2 Schemas ===


oauth2_password_bearer_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    description="Use email as the username field",
)
