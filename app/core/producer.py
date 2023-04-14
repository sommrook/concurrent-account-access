from confluent_kafka import Producer, SerializingProducer
from app.core.settings import KAFKA_BOOTSTRAP
from confluent_kafka.serialization import StringSerializer


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.instance
        except AttributeError:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.instance


class Queue(object, metaclass=Singleton):
    def __init__(self):
        _conf = {
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "client.id": "42maru",
            "message.timeout.ms": 1000000,
            "linger.ms": 100,
            "key.serializer": StringSerializer('utf_8'),
            "value.serializer": StringSerializer('utf_8')
        }
        self.producer = SerializingProducer(_conf)

    def produce(self, topic, data):
        self.producer.produce(topic=topic, value=data)
        self.producer.flush()


producer = Queue()