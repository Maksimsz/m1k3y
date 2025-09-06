import logging
from ..nlp.model import query_local_model
from ..nlp.parser import parse_llm_json
from ..security.risk import classify_risk
from ..security.confirmation import needs_confirmation
from ..actions.registry import execute

logger = logging.getLogger(__name__)

class Dispatcher:
    def __init__(self, cfg, tts_fn):
        self.cfg = cfg
        self.tts_fn = tts_fn

    def handle(self, text: str):
        raw = query_local_model(self.cfg.model_name, text)
        parsed = parse_llm_json(raw)
        risk = classify_risk(parsed["intent"], parsed["action"], parsed["text"], parsed.get("risk_hint",""))
        parsed["risk"] = risk
        logger.info(f"Parsed: {parsed}")
        if parsed["intent"] == "chat":
            self.tts_fn(parsed["text"] or "Okay.")
            return
        if parsed["intent"] == "type_text":
            if not self.cfg.enable_text_injection:
                self.tts_fn("Text injection disabled.")
                return
        if needs_confirmation(risk, self.cfg):
            self.tts_fn(f"This is a {risk} risk action. Please confirm.")
            # For simplicity, rely on GUI confirmation (could add voice Y/N)
            from ..ui.confirmation_dialog import confirm_action
            if not confirm_action(f"Allow action '{parsed['action']}'?"):
                self.tts_fn("Cancelled.")
                return
        result = execute(parsed["action"], target=parsed.get("target"), text=parsed.get("text"))
        self.tts_fn(parsed.get("text") or "")
        if result:
            logger.info(f"Action result: {result}")