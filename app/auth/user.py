from fastapi import APIRouter, Depends
from app.models.users import UserData
from app.auth.utils import current_active_user
from typing import Annotated


router = APIRouter(prefix='/me', tags=['Users'])


@router.get("/me")
def get_user(user: Annotated[UserData, Depends(current_active_user)]):
    """Get current user information
    Parameters
    ----------
    user : Annotated[UserData, Depends(current_active_user)]
        Current active user data
    Returns
    -------
    UserData
        Current active user data
    """
    return user
