from logging import getLogger
from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError

from .blacklist import JwtBlacklist
from .exceptions import ExpiredTokenError, InvalidTokenError, RevokedTokenError

# =============================================================================
# Get Logger.
# =============================================================================


logger = getLogger(__name__)


# =============================================================================
# Jwt Token Verifier.
# =============================================================================


class JwtVerifier:
    def __init__(self, blacklist: JwtBlacklist) -> None:
        self.blacklist = blacklist

    async def verify_token(
        self, *, token: str, expected_sub: str, secret_key: str, algorithm: str
    ) -> dict[str, Any]:
        try:
            claims = jwt.decode(
                token=token,
                key=secret_key,
                algorithms=[algorithm],
            )
        except ExpiredSignatureError as exc:
            logger.debug("Expired Jwt", exc_info=exc)
            raise ExpiredTokenError("Jwt token signature expire.")
        except JoseJWTError as exc:
            logger.debug("Invalid Jwt", exc_info=exc)
            raise InvalidTokenError("Invalid jwt token.")

        self._validate_claims(claims)
        self._validate_subject(claims, expected_sub)
        await self._validate_not_revoked(claims)

        return claims

    @staticmethod
    def _validate_claims(claims: dict[str, Any]) -> None:
        required = {"sub", "exp", "iat", "jti"}
        if not required.issubset(claims):
            raise InvalidTokenError(
                "Jwt verification failed by missing required claims."
            )

    @staticmethod
    def _validate_subject(claims: dict[str, Any], expected_sub: str) -> None:
        if claims["sub"] != expected_sub:
            raise InvalidTokenError("Jwt verification failed because subject mismatch.")

    async def _validate_not_revoked(self, claims: dict[str, Any]) -> None:
        if await self.blacklist.is_revoked(jti=claims["jti"]):
            raise RevokedTokenError("Jwt verification failed because token revoked.")
