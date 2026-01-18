from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.oauth2 import oauth2_password_bearer_schema

# === OAuth2 Deps ===

OAuth2PasswordBearerDep = Annotated[str, Depends(oauth2_password_bearer_schema)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
