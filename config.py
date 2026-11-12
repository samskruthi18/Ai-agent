import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Add it to .env")
llm = LLM(
    model=os.getenv("GEMINI_MODEL", "gemini/gemini-3.5-flash-lite"),
    api_key=API_KEY,
    temperature=0.2,
)
