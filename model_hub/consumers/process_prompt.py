import json
import os
from core.kafka_utils.consumer import KafkaConsumerWrapper
from core.aws_utils.storage import generate_presigned_url
from ..services.instruction_loader import get_instruction
from ..services.model_client import send_request


def process_message(key, value):
    try:
        data = json.loads(value)
        print(f"📩 Received: {data}")

        # 1️⃣ Get instruction
        instruction = instruction = get_instruction("analyze_invoice")
        if not instruction:
            print("❌ Instruction not found!")
            return

        # 2️⃣ If a file is included, get it from S3
        if "attachment_location" in data:
            psurl = generate_presigned_url(data["attachment_location"])

        print (instruction)
        # 3️⃣ Send request to OpenAI
        result = send_request(
            instruction,
            prompt_text=data.get("prompt"),
            file_url=psurl,  # Pass URL directly
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