from core.exceptions import AppError


class JwtError(AppError):
    """Base JWT-related exception"""

    pass


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class RevokedTokenError(JwtError):
    pass
