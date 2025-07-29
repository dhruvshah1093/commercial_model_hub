import os
from confluent_kafka import Producer


class KafkaProducerWrapper:
    """Reusable Kafka Producer wrapper"""

    def __init__(self, bootstrap_servers=None):
        # Get from env OR fallback to kafka:9092
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BROKER", "kafka:9092")
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def _delivery_report(self, err, msg):
        """Delivery callback"""
        if err is not None:
            print(f"❌ Delivery failed: {err}")
        else:
            print(f"✅ Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def send(self, topic: str, key: str, value: str):
        """Send a message to Kafka"""
        try:
            self.producer.produce(
                topic=topic,
                key=key.encode("utf-8") if key else None,
                value=value.encode("utf-8"),
                callback=self._delivery_report
            )
            self.producer.flush()
        except Exception as e:
            print(f"⚠️ Kafka send error: {e}")


# from core.kafka_utils.producer import KafkaProducerWrapper

producer = KafkaProducerWrapper()
producer.send("test-topic", key="order-1", value="Order created successfully!")
