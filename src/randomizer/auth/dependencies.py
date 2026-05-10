from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..auth.service import get_current_user
from ..schemas import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_from_header(token: str = Depends(oauth2_scheme)) -> UserInDB:
    return get_current_user(token)