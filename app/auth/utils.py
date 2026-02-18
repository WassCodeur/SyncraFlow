from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256

from app.stockage import load_data, MOCK_USERS, save_data
from datetime import timezone, datetime, timedelta
from app.models.users import Token
from typing import Annotated
from app.models.users import UserData
from app.core.config import get_config


OAuth2_token = OAuth2PasswordBearer(tokenUrl="/auth/token")

fake_db = load_data()
config = get_config()


def hash_password(plaint_password):
    """ Hash a plain password using pbkdf2_sha256 algorithm.

    Parameters
    ----------
    plaint_password : str
        The plain password to hash.

    Returns
    -------
    str
        The hashed password.
    """
    return pbkdf2_sha256.hash(plaint_password)


def verify_password(plaint_password, password_hash):
    """ Verify a plain password against a hashed password.

    Parameters
    ----------
    plaint_password : str
        The plain password to verify.
    password_hash : str
        The hashed password to compare against.

    Returns
    -------
        bool
        True if the password is correct, False otherwise.
    """

    return pbkdf2_sha256.verify(plaint_password, password_hash)


def get_user(username):
    """ Retrieve a user from the fake database by username.

    Parameters
    ----------
    username : str
        The username of the user to retrieve.

    Returns
    -------
    dict or None
        The user data if found, None otherwise.
    """
    # TODO: Implement a more efficient way to retrieve user data, such as using a database or an in-memory data structure
    for user in fake_db:
        if user['username'] == username:
            return user

    return None


def authentication(username, password):
    """Authenticate a user by username and password.

    Parameters
    ----------
    username : str
        The username of the user to authenticate.
    password : str
        The plain password of the user to authenticate.

    Returns
    -------
    dict
        The user data if authentication is successful, None otherwise.

    Raises
    ------
    HTTPException
        If authentication fails due to incorrect username or password.
    """
    # TODO: Implement a more secure authentication mechanism, such as using a database with hashed passwords and salting
    AUTH_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Password or username incorrect"
    )
    user = get_user(username)
    if user:
        if verify_password(password, user['password_hash']):
            return user

    raise AUTH_ERROR


def create_access_token(data, expire=config.access_token_expire_minutes):
    """Create a JWT access token with the given data and expiration time.

    Parameters
    ----------
    data : dict
        The data to include in the token payload.
    expire : int, optional
        The expiration time of the token in minutes (default is ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns
    -------
    Token
        An instance of the Token model containing the access token and token type.

    Raises
    ------
    HTTPException
        If token creation fails due to any reason.
    """
    # TODO: Implement a more robust token creation mechanism, such as using a secure key management system and handling potential exceptions during token encoding
    to_encode = data.copy()
    TOKEN_CREATION_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to create token"
    )

    try:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expire)
        to_encode['exp'] = exp
        access_token = encode(
            to_encode, config.secret_key, algorithm=config.algorithm)

        return Token(access_token=access_token, token_type="bearer")

    except Exception:
        raise TOKEN_CREATION_ERROR


async def current_user(token: Annotated[str, Depends(OAuth2_token)]):
    """ Get the current user based on the provided JWT token

    Parameters
    ----------
    token : str
        The JWT token provided in the request header

    Returns
    -------
    UserData
        The user data if the token is valid
    Raises
    ------
    HTTPException
        If credential verification fails or the token is invalid
    """
    # TODO: Implement a more secure token verification mechanism, such as using a secure key management system and handling potential exceptions during token decoding
    CREDENTIAL_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credential verification failed"
    )

    try:

        playload = decode(token, config.secret_key,
                          algorithms=[config.algorithm])
        username = playload.get('sub')

        if username is None:
            raise CREDENTIAL_ERROR

        user = get_user(username)

        if user is None:
            raise CREDENTIAL_ERROR

        user = UserData(**user)

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired"
        )

    except InvalidTokenError:
        raise CREDENTIAL_ERROR


async def current_active_user(current: Annotated[UserData, Depends(current_user)]):
    """ Get the current active user

    Parameters
    ----------
    current : Annotated[UserData, Depends(current_user)]
        The current user data obtained from the token
    Returns
    -------
    UserData
        The current active user data
    Raises
    ------
    HTTPException
        If the user is not active
    """
    # TODO: Implement a more robust user activity check, such as using a database field to track user activity status and handling potential exceptions during the check
    INACTIVE_USER = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="inactive user"
    )
    if not current.is_active:
        raise INACTIVE_USER

    return current


def register_user(data):
    """ Register a new user

    Parameters
    ----------
    data : dict
        The user data to register
    """
    fake_db.append(data)
    save_data(fake_db)
