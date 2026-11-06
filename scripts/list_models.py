import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
load_dotenv()

from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

candidates = [
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

print("Testing which models respond right now:\n")
for model in candidates:
    try:
        res = client.models.generate_content(
            model=model,
            contents="Say 'OK' in one word.",
        )
        print(f"✅ {model}: SUCCESS -> '{res.text.strip()}'")
    except Exception as e:
        err = str(e)
        if "503" in err:
            status = "503 (High Demand)"
        elif "404" in err:
            status = "404 (Not Found)"
        else:
            status = f"Error: {err[:60]}"
        print(f"❌ {model}: {status}")
