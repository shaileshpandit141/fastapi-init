from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import oauth2_scheme

Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
