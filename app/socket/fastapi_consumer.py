import asyncio
import os
import aiokafka
import json

from app.core.settings import CONSUMER_SOCKET_GROUP, KAFKA_SOCKET_TOPIC, KAFKA_BOOTSTRAP
from app.core.log_manager import access_logger
from app.socket.socket_handler import sio, login_namespace


async def socket_consumer():
    loop = asyncio.get_event_loop()
    global consumer
    consumer_group = f"{CONSUMER_SOCKET_GROUP}_{os.getpid()}"
    consumer = aiokafka.AIOKafkaConsumer(KAFKA_SOCKET_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP, group_id=consumer_group)
    access_logger.info(f"consumer group start {consumer_group} | {KAFKA_SOCKET_TOPIC}")
    await consumer.start()


async def send_consumer_message():
    access_logger.info(f"send consumer message start")
    try:
        async for msg in consumer:
            value = json.loads(msg.value)
            if value.get("namespace") == login_namespace:
                await sio.emit(event=value.get("event"), data=value.get("data"), namespace=login_namespace,
                               room=value.get("room"), skip_sid=value.get("skip_sid"))
            await consumer.commit()
    finally:
        access_logger.warning("Stopping consumer")
        await consumer.stop()
