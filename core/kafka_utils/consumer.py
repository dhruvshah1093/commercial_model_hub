import os
import json
from confluent_kafka import Consumer, KafkaError


class KafkaConsumerWrapper:
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
        print(f"Listening to topic '{self.topic}' on {self.bootstrap_servers}...\n")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Error: {msg.error()}")
                        continue

                key = msg.key().decode("utf-8") if msg.key() else None
                value = msg.value().decode("utf-8")

                if process_callback:
                    
                    process_callback(key, value)
                else:
                    print(f" Received: Key={key} | Value={value} | Partition={msg.partition()} Offset={msg.offset()}")

        except KeyboardInterrupt:
            print("\n Stopping consumer...")
        finally:
            self.consumer.close()


# 🔁 Your callback function — will be triggered for each Kafka message
def callbackFunction(key, value):
    print("\n🔄 Callback function called")

    try:
        message = json.loads(value)
        event = message.get("event")
        data = message.get("data")

        if event == "prompt_created" and data:
            print(f"Routing prompt ID {data.get('id')}")
            route_prompt(data)  # <-- Call your routing logic here
        else:
            print(f"Unsupported event type or malformed message: {event}")

    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {value}")
    except Exception as e:
        print(f"Error during callback: {e}")


def route_prompt(data):
    print(f"Route this prompt: {data['prompt']}")
    # Receving the details here
    # SQL,Files,AI-models -Fallback Systems
    # Langchain For SQL (verified, time-scanned)
    # LangGraph For Routing to SQL or Files or AI-models

    # You can plug in LangChain SQL checker here, or call another microservice


if __name__ == "__main__":
    consumer = KafkaConsumerWrapper(topic="prom")
    consumer.consume_messages(callbackFunction)
