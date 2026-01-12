from core.exceptions import AppError


class JwtError(AppError):
    pass


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class RevokedTokenError(JwtError):
    pass
