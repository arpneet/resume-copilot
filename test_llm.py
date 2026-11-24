import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=20000),
)

models = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
]

for name in models:
    start = time.time()
    try:
        r = client.models.generate_content(
            model=name,
            contents="Reply with the single word: hello",
        )
        print(f"OK    {name}: {r.text!r} ({time.time() - start:.1f}s)")
    except Exception as e:
        print(f"FAIL  {name}: {type(e).__name__} ({time.time() - start:.1f}s)")
