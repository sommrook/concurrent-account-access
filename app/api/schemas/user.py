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
    created_date: Optional[str]
    updated_date: Optional[str]


class LoginResponse(BaseModel):
    response_code: str
    response_message: str
    token: Optional[Token]
    user: Optional[UserInfo]


class LoginRequest(BaseModel):
    user_account: str
    password: str