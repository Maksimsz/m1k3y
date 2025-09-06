import logging

logger = logging.getLogger(__name__)

def needs_confirmation(risk_level: str, config):
    if risk_level == "high":
        return True
    if risk_level == "medium":
        return not config.auto_confirm_medium
    return not config.auto_confirm_low