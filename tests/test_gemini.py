
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API KEY NOT FOUND")
    raise SystemExit

print("API key loaded.")
print("Connecting to Gemini...")

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=15000
        )
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with exactly: Gemini is working!",
        config=types.GenerateContentConfig(
            max_output_tokens=30
        )
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nCONNECTION FAILED")
    print(type(e).__name__)
    print(e)
