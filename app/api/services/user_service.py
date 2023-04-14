import re
import bcrypt
import jwt
from datetime import timedelta, datetime

from app.db.repositories.user_repository import UserRepository
from app.db.models.user import User
from app.db.models.account_access import AccountAccess
from app.api.schemas.user import *

from app.core.settings import SECRET_KEY, ALGORITHM
from app.core.status_code import StatusCode

from app.socket.socket_handler import sio, login_namespace


class UserService(object):
    def __init__(self):
        self.user_repo = UserRepository

    @staticmethod
    def dateformat(date: datetime):
        return date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_token(self, find_user):
        access_token_expires = timedelta(days=7)
        access_token = self.create_access_token(
            data={"user_id": find_user.user_uuid.decode(), "user_account": find_user.user_account,
                  "created_date": self.dateformat(find_user.created_date),
                  "pwd_updated_date": self.dateformat(find_user.pwd_updated_date)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def login_user(self, db, request: LoginRequest, ip_address):
        if not request.user_account:
            return "MUST_HAVE_ENTER_ACCOUNT"
        if not request.password:
            return "MUST_HAVE_ENTER_PASSWORD"
        find_user = self.user_repo.find_user_by_account(db, request.user_account)
        if not find_user:
            return "USER_NOT_FOUND"
        if not bcrypt.checkpw(request.password.encode('utf-8'), find_user.password.encode('utf-8')):
            return "INVALID_PASSWORD"
        return LoginResponse(
            response_code=StatusCode.CODE2000.code,
            response_message=StatusCode.CODE2000.message,
            token=Token(**self.create_token(find_user)),
            user=UserInfo(
                user_id=find_user.user_id,
                user_account=find_user.user_account,
                email=find_user.email,
                ip_address=ip_address,
                created_date=self.dateformat(find_user.created_date) if find_user.created_date else None,
                updated_date=self.dateformat(find_user.updated_date) if find_user.updated_date else None
            )
        )

    async def logout_user(self, db, request: LogoutRequest, ip_address):
        pass

    async def create_user(self, db, request: CreateUserRequest):
        # 1. account 중복 체크
        # 2. password 처리 규칙
        user_account = request.user_account
        password = request.password

        find_user = self.user_repo.find_user_by_account(db, user_account)
        if find_user:
            return "ALREADY_EXISTS"
        if len(user_account) < 4 or len(user_account) > 20:
            return "INVALID_ACCOUNT_LEN"
        if user_account.find(" ") != -1:
            return "ACCOUNT_CONTAINS_BLANK"

        regex = re.compile(
            r"^[A-Za-z\d`~!@#$%^&*()–_=+\[{}\]:;\',.?/<>]{8,20}"
        )
        if not re.fullmatch(regex, password):
            return "INVALID_PASSWORD_FORMAT"
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if not re.fullmatch(regex, request.email):
            return "INVALID_EMAIL"

        user = User(
            user_account=user_account,
            password=password,
            user_name=request.user_name,
            email=request.email,
        )
        db.add(user)
        db.commit()
        return "OK"
