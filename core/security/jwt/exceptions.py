from core.exceptions import AppException


class JwtException(AppException):
    """Base JWT-related exception"""

    pass


class InvalidTokenException(JwtException):
    pass


class ExpiredTokenException(JwtException):
    pass


class RevokedTokenException(JwtException):
    pass
