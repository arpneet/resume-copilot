import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=60000),  # 60 seconds
)

# Tried in order. If one is overloaded, the next one is used.
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]


def call_llm_json(system: str, user: str, max_tokens: int = 8000) -> dict:
    last_error = None
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=user,
                    config={
                        "system_instruction": system,
                        "max_output_tokens": max_tokens,
                        "response_mime_type": "application/json",
                    },
                )
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.text.strip())
                return json.loads(text)
            except errors.ServerError as e:  # 503 etc.: wait, then retry
                last_error = e
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
            except Exception as e:  # timeouts, bad JSON: move to next attempt
                last_error = e
                time.sleep(1)
    raise RuntimeError(f"All models failed. Last error: {last_error}")