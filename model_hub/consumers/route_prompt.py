import json
import os
from core.kafka_utils.consumer import KafkaConsumerWrapper
from core.aws_utils.storage import generate_presigned_url
from ..services.instruction_loader import get_instruction
from ..services.model_client import send_request
from ..services.generate_sql import can_generate_sql, run_sql_chain

def route_prompt(key, data):
    message = json.loads(data)
    event = message["event"]
    content = message["data"]
    prompt = content["prompt"]
    group_id = content["group_id"]
    attachment_location = content["attachment_location"]

    print(f"Routing prompt '{prompt}' for group {group_id}")

    # 1️⃣ Try SQL path
    if can_generate_sql(prompt):
        sql_result = run_sql_chain(prompt, group_id)
        print(sql_result)
        if is_sql_result_sufficient(sql_result):
            print("✅ SQL result sufficient, sending to result handler...")
            send_to_result(sql_result, data)
            return
    return
    # 2️⃣ If SQL fails or insufficient, check attachments
    if attachment_location:
        print("📂 Attachment found, running file extraction...")
        file_info = run_file_extraction(attachment_location)
        final_response = run_ai_with_context(prompt, file_info)
    else:
        print("⚠️ No attachment, falling back to direct AI...")
        final_response = run_ai_without_file(prompt)

    # 3️⃣ Store/send final response
    send_to_result(final_response, data)


# def run_sql_chain(prompt, group_id):
#     """Stub: Replace with LangChain SQLDatabaseChain"""
#     return {}

# def is_sql_result_sufficient(sql_result):
#     """Stub: Replace with real evaluation"""
#     return False

# def run_file_extraction(attachment_location):
#     """Stub: Replace with OCR, Gemini, Claude, etc."""
#     return "Extracted file text here"

# def run_ai_with_context(prompt, context):
#     """Stub: Combine prompt with extracted context, run AI"""
#     return f"AI answer using context: {context}"

# def run_ai_without_file(prompt):
#     """Stub: Direct AI call without extra context"""
#     return f"AI answer to prompt: {prompt}"

# def send_to_result(result, original_data):
#     """Stub: Push final result to Kafka or update DB"""
#     print(f"📤 Final result for {original_data['id']}: {result}")
    
# LangGraph code to route to different processes 
def main():
    topic_name = os.getenv("KAFKA_TOPIC", "prompts")
    group_id = os.getenv("KAFKA_GROUP_ID", "router")
    consumer = KafkaConsumerWrapper(topic=topic_name,group_id=group_id)
    consumer.consume_messages(process_callback=route_prompt)


if __name__ == "__main__":
    main()


