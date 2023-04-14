import json

import socketio
from app.core.log_manager import access_logger
from app.db.session import get_db
from app.db.models.account_access import AccountAccess
from app.db.repositories.user_repository import UserRepository
from app.core.producer import producer
from app.core.settings import KAFKA_SOCKET_TOPIC

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

login_namespace = "/login"

def login_socket_handler():
    @sio.event(namespace=login_namespace)
    async def connect(sid, environ):
        access_logger.info(f"login connect")

    @sio.event(namespace=login_namespace)
    async def disconnect(sid):
        access_logger.info(f"login disconnect")

    @sio.on("login", namespace=login_namespace)
    async def login(sid, data):
        data = json.loads(data)
        user_id = data["user_id"]
        user_account = data["user_account"]
        ip_address = data["ip_address"]
        db = next(get_db())
        find_users = UserRepository.find_user_by_login_id(db, user_id)
        ip_list = list(set([user.ip_address for user in find_users]))
        if ip_address in ip_list:
            ip_list.remove(ip_address)
        await sio.emit(event="login-user", data=ip_list, to=sid, namespace=login_namespace, callback=None)

        await sio.enter_room(sid, namespace=login_namespace, room=user_account)
        account_access = AccountAccess(
            user_id=user_id,
            ip_address=ip_address,
            sid=sid
        )
        db.add(account_access)
        db.commit()

        data = {
            "namespace": login_namespace,
            "event": "other-login",
            "data": ip_address,
            "room": user_account,
            "skip_sid": sid
        }
        producer.produce(topic=KAFKA_SOCKET_TOPIC, value=json.dumps(data))

