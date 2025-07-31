import os
import json
import requests
from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"

def to_curl(url, method="POST", headers=None, json_data=None):
    """
    Converts a requests call to a curl command string.

    :param url: API endpoint URL
    :param method: HTTP method (default: POST)
    :param headers: dict of headers
    :param json_data: dict to be sent as JSON
    :return: cURL command string
    """

    cmd = ["curl", "-X", method.upper(), f"\"{url}\""]

    if headers:
        for key, value in headers.items():
            cmd.append(f"-H \"{key}: {value}\"")

    if json_data:
        json_str = json.dumps(json_data, ensure_ascii=False)
        cmd.append(f"-d '{json_str}'")

    return " \\\n  ".join(cmd)

def send_request(instruction, prompt_text=None, file_url=None, overrides=None):
    """
    Sends a request to OpenAI dynamically with optional file URL (no file upload needed).
    Matches the CURL format you shared.

    :param instruction: dict → contains 'model', 'description', 'temperature', etc.
    :param prompt_text: str → User prompt
    :param file_url: str or None → Publicly accessible file URL (S3 URL works if not private)
    :param overrides: dict → Runtime overrides for model, temperature, etc.
    """

    model = overrides.get("model") if overrides else instruction.get("model", "gpt-4.1")
    temperature = overrides.get("temperature") if overrides else instruction.get("temperature", 0.3)

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    final_prompt = instruction["description"]
    if prompt_text:
        final_prompt += f"\n\nUser prompt:\n{prompt_text}"

    # Build content array
    content = [{"type": "input_text", "text": final_prompt}]
    if file_url:
        content.append({"type": "input_image", "image_url": file_url})

    payload = {
        "model": model,
        "temperature": temperature,
        "input": [{"role": "user", "content": content}],
    }
    print (to_curl(f"{BASE_URL}/responses","POST",headers,payload))
    response = requests.post(f"{BASE_URL}/responses", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
