from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from datetime import datetime, timezone

ROLES = ["SUPER_ADMIN", "ADMIN", "DEVELOPER", "USER"]


class User(BaseModel):
    username: str


class UserLogin(User):
    password: str


class UserData(User):
    name: str
    email: EmailStr
    tier: str
    is_active: bool


class UserRegistered(UserLogin):
    id: UUID = Field(uuid4())
    name: str
    email: EmailStr
    tier: str = "free"


class Token(BaseModel):
    access_token: str
    token_type: str = Field("bearer")
