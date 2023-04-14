from datetime import datetime

from app.db.session import Base

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)

class AccountAccess(Base):
    __tablename__ = "account_access"

    access_id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("auth_user.user_id", ondelete="CASCADE"), index=True)
    ip_address: str = Column(String(32))
    sid: str = Column(String(32))