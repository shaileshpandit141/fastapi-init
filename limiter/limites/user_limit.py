from typing import Literal

from fastapi import Request

from dependencies.auth.user import CurrentUserDep


def get_user_limit(request: Request, user: CurrentUserDep) -> Literal["10/minute"]:
    # if user.role == "admin":
    #     return "1000/minute"
    return "10/minute"
