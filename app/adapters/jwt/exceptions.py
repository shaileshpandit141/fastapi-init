from app.core.exceptions.domain import DomainError

# =============================================================================
# Jwt Errors
# =============================================================================


class JwtError(DomainError):
    """Base JWT-related exception"""

    pass


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class RevokedTokenError(JwtError):
    pass
