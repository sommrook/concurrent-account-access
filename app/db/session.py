import base64
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from core.settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, \
    IS_CYPER, KEY, IV


class AESCipher(object):
    def __init__(self, key, iv):
        self.key = key.encode(encoding="utf-8")
        self.iv = iv.encode(encoding="utf-8")
        self.pad = 16

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message, self.pad)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = cipher.decrypt(enc)
        return unpad(dec, 16).decode('utf-8')


USER = MYSQL_USER
PASSWORD = MYSQL_PASSWORD
if IS_CYPER:
    aes = AESCipher(KEY, IV)
    oracle_user = aes.decrypt(MYSQL_USER)
    oracle_password = aes.decrypt(MYSQL_PASSWORD)


link = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}:{MYSQL_DATABASE}"
engine = create_engine(link, echo=False, pool_pre_ping=True, encoding="utf-8", convert_unicode=False,
                       pool_recycle=3600, pool_size=50, max_overflow=20, max_identifier_length=30)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base(bind=engine)

def get_db() -> Generator:
    db = Session()
    try:
        yield db
    finally:
        db.close()
