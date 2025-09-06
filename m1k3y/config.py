from pydantic import BaseModel, Field
from pathlib import Path
import json
from platformdirs import user_config_dir
from typing import Optional

class AppConfig(BaseModel):
    model_name: str = Field(default="mistral")
    mic_device_index: Optional[int] = None
    tts_voice: Optional[str] = None
    enable_text_injection: bool = True
    auto_confirm_low: bool = True
    auto_confirm_medium: bool = False
    require_voice_confirm_high: bool = True
    log_level: str = "INFO"

CONFIG_DIR = Path(user_config_dir("m1k3y", "local"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = CONFIG_DIR / "user_config.json"

def load_config() -> AppConfig:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return AppConfig(**data)
        except Exception:
            pass
    cfg = AppConfig()
    save_config(cfg)
    return cfg

def save_config(cfg: AppConfig):
    CONFIG_PATH.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")