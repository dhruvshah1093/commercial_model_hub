import os
from confluent_kafka import Consumer, KafkaError


class KafkaConsumerWrapper:
    """Reusable Kafka Consumer wrapper with support for custom message processing"""

    def __init__(self, topic, group_id="default-group", bootstrap_servers=None):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BROKER", "kafka:9092")

        conf = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }

        self.consumer = Consumer(conf)
        self.consumer.subscribe([self.topic])

    def consume_messages(self, process_callback=None):
        """
        Starts consuming messages. Calls process_callback(key, value) for each message.
        If process_callback is None, only prints the messages.
        """
        print(f"🚀 Listening to topic '{self.topic}' on {self.bootstrap_servers}...\n")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"❌ Error: {msg.error()}")
                        continue

                key = msg.key().decode("utf-8") if msg.key() else None
                value = msg.value().decode("utf-8")

                if process_callback:
                    process_callback(key, value)
                else:
                    print(f"✅ Received: Key={key} | Value={value} | Partition={msg.partition()} Offset={msg.offset()}")

        except KeyboardInterrupt:
            print("\n🛑 Stopping consumer...")
        finally:
            self.consumer.close()

def callbackFunction(key, value):
    print ("\n Callback function called")

if __name__ == "__main__":
    topic_name = os.getenv("KAFKA_TOPIC", "test-topic")
    group_id = os.getenv("KAFKA_GROUP_ID", "test-consumer-group")
    consumer = KafkaConsumerWrapper(topic=topic_name, group_id=group_id)
    consumer.consume_messages(process_callback=callbackFunction)