from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.security.auth import oauth2_scheme

Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
