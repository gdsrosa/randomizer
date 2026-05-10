from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..database import users_db
from ..schemas import UserCreate, UserInDB, UserResponse
from ..auth.service import authenticate_user, get_password_hash, refresh_access_token, get_current_user
from .schemas import LoginRequest, RefreshTokenRequest, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    existing = users_db.get_by_username(user.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(id=user.id, username=user.username, hashed_password=hashed_password)
    users_db.add(new_user)

    return UserResponse(id=new_user.id, username=new_user.username)


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    return authenticate_user(login_data)


@router.post("/refresh", response_model=Token)
def refresh(token_data: RefreshTokenRequest):
    return refresh_access_token(token_data.refresh_token)


def get_current_user_from_header(token: str = Depends(oauth2_scheme)) -> UserInDB:
    return get_current_user(token)