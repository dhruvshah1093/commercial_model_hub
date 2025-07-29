import os
import json
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"

def send_request(instruction, file_obj=None, overrides=None):
    """
    Sends a request to OpenAI dynamically with optional file attachment.

    :param instruction: dict → contains 'model', 'description', 'temperature', etc.
    :param file_obj: tuple or None → (filename, BytesIO, content_type)
    :param overrides: dict or None → runtime overrides for model, temperature, etc.
    """

    model = (overrides.get("model") if overrides else instruction.get("model", "gpt-4o-mini"))
    temperature = (overrides.get("temperature") if overrides else instruction.get("temperature", 0.3))

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    metadata = {
        "model": model,
        "temperature": temperature,
        "input": [
            {"role": "user", "content": [{"type": "input_text", "text": instruction["description"]}]}
        ]
    }

    # If a file is attached, send as multipart/form-data
    if file_obj:
        files = {
            "file": file_obj,  # file_obj should be (filename, BytesIO, content_type)
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        response = requests.post(f"{BASE_URL}/responses", headers=headers, files=files)
    else:
        headers["Content-Type"] = "application/json"
        response = requests.post(f"{BASE_URL}/responses", headers=headers, json=metadata)

    response.raise_for_status()
    return response.json()
