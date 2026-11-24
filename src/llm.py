import json
import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=60000),  # 60 seconds
)
MODEL = "gemini-3.5-flash-lite"


def call_llm_json(system: str, user: str, max_tokens: int = 8000) -> dict:
    response = client.models.generate_content(
        model=MODEL,
        contents=user,
        config={
            "system_instruction": system,
            "max_output_tokens": max_tokens,
            "response_mime_type": "application/json",
        },
    )
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.text.strip())
    return json.loads(text)