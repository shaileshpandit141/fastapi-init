class JWTError(Exception):
    """Base JWT error."""


class InvalidTokenError(JWTError):
    pass


class ExpiredTokenError(JWTError):
    pass


class RevokeTokenError(JWTError):
    pass
