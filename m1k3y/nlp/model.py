import requests
import logging
from ..constants import OLLAMA_ENDPOINT

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are M1K3Y local assistant. 
Return a JSON object with fields:
intent: one of [chat, system_command, type_text]
action: short verb or command
target: optional target (file/app)
text: response to speak or type
risk_hint: guess risk level low/medium/high
If user asks to 'type' or 'write', choose intent=type_text.
Only output JSON.
"""

def query_local_model(model_name: str, user_text: str):
    payload = {
        "model": model_name,
        "prompt": f"{SYSTEM_PROMPT}\nUser: {user_text}\nAssistant JSON:",
        "stream": False
    }
    try:
        r = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip()
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return '{"intent":"chat","text":"I had a local processing error.","action":""}'