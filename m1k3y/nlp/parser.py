import json
import logging

logger = logging.getLogger(__name__)

def parse_llm_json(raw: str):
    try:
        # Some models may prepend text: attempt to isolate JSON
        start = raw.find('{')
        end = raw.rfind('}')
        snippet = raw[start:end+1]
        data = json.loads(snippet)
        return {
            "intent": data.get("intent", "chat"),
            "action": data.get("action", ""),
            "target": data.get("target"),
            "text": data.get("text", ""),
            "risk_hint": data.get("risk_hint", "low").lower()
        }
    except Exception as e:
        logger.warning(f"Parse failure: {e} raw={raw[:120]}")
        return {"intent": "chat", "text": raw, "action": "", "risk_hint": "low"}