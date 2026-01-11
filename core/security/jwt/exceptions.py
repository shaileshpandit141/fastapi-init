from core.exceptions import AppError


class JWTError(AppError):
    pass


class InvalidTokenError(JWTError):
    pass


class ExpiredTokenError(JWTError):
    pass


class RevokedTokenError(JWTError):
    pass
