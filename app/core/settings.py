import os

# API
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8000))
API_WORKERS = int(os.environ.get("API_WORKERS", 3))

# LOG
LOG_PATH = "/logs"

# JWT KEY
SECRET_KEY = "sksmdmdmsdlekzmfthadlq"
ALGORITHM = "HS256"

# DB
MYSQL_USER = os.environ.get("MYSQL_USER", "rEgT6+Cxrdz4g6U+0uIaJw==")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "XCOFnUHPrMaUBYKY1t15ag==")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "concurrent_access")

# cyper -> 32 / 16
KEY = os.environ.get("KEY", "sksmsdlekhadlqdfegslkzmffhdldldq")
IV = os.environ.get("IV", "dlekthadlqslekzm")
IS_CYPER = int(os.environ.get("IS_CYPER", 1))

# KAFKA
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_HOST", "localhost:9092")
KAFKA_SOCKET_TOPIC = os.environ.get("KAFKA_SOCKET_TOPIC", "socket.pub.sub")
CONSUMER_SOCKET_GROUP = os.environ.get("CONSUMER_SOCKET_GROUP", "socket_group")
