from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError

from core.security.jwt.exceptions import ExpiredTokenError, InvalidTokenError
from core.settings import settings


def _verify_jwt(
    *,
    sub: str,
    token: str,
    secret_key: str,
    algorithm: str,
) -> dict[str, Any]:
    try:
        claims = jwt.decode(
            token=token,
            key=secret_key,
            algorithms=[algorithm],
        )
    except ExpiredSignatureError:
        raise ExpiredTokenError()
    except JoseJWTError:
        raise InvalidTokenError()

    required_claims = {"sub", "exp", "iat", "jti"}
    if not required_claims.issubset(claims):
        raise InvalidTokenError()

    if claims.get("sub") != sub:
        raise InvalidTokenError()

    return claims


def verify_access_token(token: str) -> dict[str, Any]:
    return _verify_jwt(
        sub="access",
        token=token,
        secret_key=settings.access_token_secret_key,
        algorithm=settings.algorithm,
    )


def verify_refresh_token(token: str) -> dict[str, Any]:
    return _verify_jwt(
        sub="refresh",
        token=token,
        secret_key=settings.refresh_token_secret_key,
        algorithm=settings.algorithm,
    )
