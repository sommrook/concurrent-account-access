import os

API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8000))
API_WORKERS = int(os.environ.get("API_WORKERS", 3))

LOG_PATH = "/logs"

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_HOST", "localhost:9092")
KAFKA_SOCKET_TOPIC = os.environ.get("KAFKA_SOCKET_TOPIC", "socket.anno")
CONSUMER_SOCKET_GROUP = os.environ.get("CONSUMER_SOCKET_GROUP", "socket_anno_group")
