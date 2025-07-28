import os
from confluent_kafka import Consumer, KafkaError


class KafkaConsumerWrapper:
    """Reusable Kafka Consumer wrapper"""

    def __init__(self, topic, group_id="default-group", bootstrap_servers=None):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BROKER", "kafka:9092")

        conf = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",  # Start reading from the beginning if no offset is committed
        }

        self.consumer = Consumer(conf)
        self.consumer.subscribe([self.topic])

    def consume_messages(self):
        print(f"🚀 Listening to topic '{self.topic}' on {self.bootstrap_servers}...\n")
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Poll every 1 second
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"❌ Error: {msg.error()}")
                        continue

                print(f"✅ Received: Key={msg.key()} | Value={msg.value().decode('utf-8')} | Partition={msg.partition()} Offset={msg.offset()}")

        except KeyboardInterrupt:
            print("\n🛑 Stopping consumer...")
        finally:
            self.consumer.close()


if __name__ == "__main__":
    topic_name = os.getenv("KAFKA_TOPIC", "test-topic")
    consumer = KafkaConsumerWrapper(topic=topic_name, group_id="test-consumer-group")
    consumer.consume_messages()
