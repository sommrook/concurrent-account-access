import json
import requests
from sqlalchemy.exc import SQLAlchemyError

import socketio
from app.core.log_manager import access_logger
from app.db.session import get_db
from app.db.models.account_access import AccountAccess
from app.db.repositories.user_repository import UserRepository
from app.core.producer import producer
from app.core.settings import KAFKA_SOCKET_TOPIC, LOGIN_NAMESPACE

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

login_namespace = f"/{LOGIN_NAMESPACE}"

def login_socket_handler():
    @sio.event(namespace=login_namespace)
    async def connect(sid, environ):
        access_logger.info(f"login connect")

    @sio.event(namespace=login_namespace)
    async def disconnect(sid):
        try:
            db = next(get_db())
            db.query(AccountAccess).filter(
                AccountAccess.sid == sid
            ).delete(synchronize_session='fetch')
            db.commit()
            db.close()
        except SQLAlchemyError as e:
            access_logger.error(f"sqlalchemy error is {e}")

    @sio.on("login", namespace=login_namespace)
    async def login(sid, data):
        data = json.loads(data)
        access_logger.info(data)
        user_id = data["user_id"]
        user_account = data["user_account"]
        ip_address = data["ip_address"]
        room_name = f"{user_account}"
        db = next(get_db())
        find_users = UserRepository.find_user_by_login_id(db, user_id)
        ip_list = list(set([user.ip_address for user in find_users]))
        if ip_address in ip_list:
            ip_list.remove(ip_address)

        account_access = AccountAccess(
            user_id=user_id,
            ip_address=ip_address,
            sid=sid
        )
        db.add(account_access)
        db.commit()

        sio.enter_room(sid, namespace=login_namespace, room=room_name)

        data = {
            "ip_list": ip_list,
            "access_id": account_access.access_id
        }

        await sio.emit(event="login-user", data=data, to=sid, namespace=login_namespace, callback=None)

        db.close()

        data = {
            "namespace": f"{login_namespace}",
            "event": "other-login",
            "data": f"{ip_address}",
            "room": room_name,
            "skip_sid": sid
        }
        producer.produce(topic=KAFKA_SOCKET_TOPIC, data=json.dumps(data))

    @sio.on("logout", namespace=login_namespace)
    async def logout(sid, data):
        data = json.loads(data)
        db = next(get_db())
        sio.leave_room(sid, namespace=login_namespace, room=data["user_account"])
        UserRepository.delete_user_by_access_id(db, data["access_id"])
        db.close()



