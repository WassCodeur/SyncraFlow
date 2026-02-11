from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.users import UserLogin, Token, UserRegistered
from typing import Annotated
from uuid import uuid4
from datetime import datetime, timezone
from app.utils.auth_utils import create_access_token, authentication, hash_password, register_user, get_user

router = APIRouter(prefix="/auth", tags=['Authentification'])


@router.post("/token", response_model=Token)
async def loggin(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login user and return access token

    Parameters
    ----------
    data : Annotated[OAuth2PasswordRequestForm, Depends()]
        User login data from form data

    Returns
    -------
    Token
        Dict containing access token and token type
    """
    user_login = UserLogin(
        username=data.username,
        password=data.password
    )
    if authentication(user_login.username, user_login.password):
        playload = {"sub": user_login.username}
        token = create_access_token(playload)

        return token


@router.post("/register")
def registration(data: UserRegistered):
    """Register a new user

    Parameters
    ----------
    data : UserRegistered
        User registration data from request body

    Returns
    -------
    dict
        User registration status
    """
    try:
        user = get_user(data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User already exist"
            )
        user = {
            "id": str(uuid4()),
            "name": data.name,
            "username": data.username,
            "email": data.email,
            "hash_passord": hash_password(data.password),
            "is_active": False,
            "role": "USER",
            "tier": data.tier,
            "created_at": str(datetime.now(timezone.utc))
        }
        register_user(user)
    except Exception as e:
        raise e

    return user
