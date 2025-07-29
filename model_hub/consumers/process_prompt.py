import json
import os
from core.kafka_utils.consumer import KafkaConsumerWrapper
from core.aws_utils.storage import get_file_from_s3
from ..services.instruction_loader import get_instruction
from ..services.model_client import send_request


def process_message(key, value):
    try:
        data = json.loads(value)
        print(f"📩 Received: {data}")

        # 1️⃣ Get instruction
        instruction = get_instruction(data.get("instruction"))
        if not instruction:
            print("❌ Instruction not found!")
            return

        file_obj = None

        # 2️⃣ If a file is included, get it from S3
        if "file" in data:
            s3_key = data["file"].get("key")
            file_like = get_file_from_s3(s3_key)  # BytesIO
            filename = os.path.basename(s3_key)

            # Convert BytesIO to tuple for requests
            file_obj = (filename, file_like, "application/octet-stream")

        # 3️⃣ Send request to OpenAI
        result = send_request(
            instruction,
            file_obj=file_obj,  # Pass tuple instead of file path
            overrides=data.get("overrides", {})
        )

        print("✅ OpenAI Response:", result)

    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    topic_name = os.getenv("KAFKA_TOPIC", "tasks")
    group_id = os.getenv("KAFKA_GROUP_ID", "openai-consumer-group")

    consumer = KafkaConsumerWrapper(topic=topic_name, group_id=group_id)
    consumer.consume_messages(process_callback=process_message)


if __name__ == "__main__":
    main()