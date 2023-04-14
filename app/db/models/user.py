from datetime import datetime

from app.db.session import Base

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    func,
)

class User(Base):
    __tablename__ = "auth_user"

    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_account: str = Column(String(32), unique=True)
    user_name: str = Column(String(128))
    password: str = Column(String(128))
    email: str = Column(String(128))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    last_login_date: datetime = Column(DateTime(timezone=True))
    pwd_updated_date: datetime = Column(DateTime(timezone=True), default=func.now())