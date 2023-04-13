import asyncio
import os
import aiokafka
import json

from src.metadata import CONSUMER_SOCKET_GROUP, KAFKA_SOCKET_TOPIC, KAFKA_BOOTSTRAP
from src.socket.socket_handler import sio
from src.logger.log_manager import access_logger


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
            # if value.get("path") == SocketPath.ANNOTATOR:
            #     if value.get("namespace") == AnnoNameSpace.files:
            #         pass
            #     elif value.get("namespace") == AnnoNameSpace.upload:
            #         await sio.emit(event=value.get("event"), data=json.dumps(value.get("data")), namespace=upload_namespace)

            await consumer.commit()
    finally:
        access_logger.warning("Stopping consumer")
        await consumer.stop()
