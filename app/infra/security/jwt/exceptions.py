from app.shared.exceptions import AppError

# =============================================================================
# Jwt Errors
# =============================================================================


class JwtError(AppError):
    """Base JWT-related exception"""

    pass


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class RevokedTokenError(JwtError):
    pass
