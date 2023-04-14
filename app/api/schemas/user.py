from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    user_id: Optional[str]
    user_account: Optional[str]
    user_name: str
    email: str
    ip_address: str
    created_date: Optional[str]
    updated_date: Optional[str]


class LoginResponse(BaseModel):
    response_code: str
    response_message: str
    token: Token
    user: UserInfo


class LoginRequest(BaseModel):
    user_account: str
    password: str


class LogoutRequest(BaseModel):
    access_id: int
    user_id: int


class CreateUserRequest(BaseModel):
    user_account: str
    user_name: str
    password: str
    email: str
