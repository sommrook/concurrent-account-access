import asyncio

from app.socket.fastapi_consumer import socket_consumer, send_consumer_message
from app.core.log_manager import access_logger

async def consume():
    asyncio.create_task(send_consumer_message())

async def startup_event_app():
    await socket_consumer()
    await consume()

def shutdown_event_app():
    access_logger.info("shutdown socket app")