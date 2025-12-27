from typing import Annotated
from fastapi import Depends
from core.security.auth import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm


Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
