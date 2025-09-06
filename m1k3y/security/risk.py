import logging
import re

logger = logging.getLogger(__name__)

HIGH_PATTERNS = [
    r"\bshutdown\b",
    r"\bdelete\b",
    r"\bformat\b",
    r"\bremove\b.*\b(system|windows|root)\b"
]

MEDIUM_PATTERNS = [
    r"\bopen\b",
    r"\blaunch\b",
    r"\btype\b",
    r"\bwrite\b"
]

def classify_risk(intent: str, action: str, text: str, model_hint: str):
    content = " ".join([intent, action, text, model_hint]).lower()
    for pat in HIGH_PATTERNS:
        if re.search(pat, content):
            return "high"
    for pat in MEDIUM_PATTERNS:
        if re.search(pat, content):
            return "medium"
    return "low"