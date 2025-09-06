from typing import Callable, Dict
from . import system_actions
from . import typing_actions

ACTION_REGISTRY: Dict[str, Callable] = {
    "time": system_actions.get_time,
    "shutdown": system_actions.shutdown_system,
    "open": system_actions.open_app,
    "list": system_actions.list_dir,
    "type_text": typing_actions.inject_text
}

def execute(action: str, target=None, text=None):
    fn = ACTION_REGISTRY.get(action)
    if not fn:
        return f"Unknown action: {action}"
    if action == "open":
        return fn(target)
    if action == "list":
        return fn(target)
    if action == "type_text":
        return fn(text or "")
    return fn()