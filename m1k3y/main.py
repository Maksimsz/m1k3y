import threading
import logging
import time
import json
import tkinter as tk
import pyttsx3

from .config import load_config
from .utils.logging_config import setup_logging
from .audio.listener import AudioStream
from .audio.transcriber import Transcriber
from .constants import TRIGGER_WORD
from .agent.dispatcher import Dispatcher
from .ui.settings_window import SettingsWindow

logger = logging.getLogger(__name__)

def tts_engine():
    engine = pyttsx3.init()
    def speak(text: str):
        if not text:
            return
        engine.say(text)
        engine.runAndWait()
    return speak

def open_settings(cfg, dispatcher):
    root = tk.Tk()
    SettingsWindow(root, cfg, on_update=lambda new_cfg: None)
    root.mainloop()

def main():
    cfg = load_config()
    setup_logging(cfg.log_level)
    speaker = tts_engine()
    speaker("Mikey online.")
    transcriber = Transcriber()
    audio = AudioStream(device=None)
    dispatcher = Dispatcher(cfg, speaker)

    should_stop = threading.Event()

    def console_commands():
        while not should_stop.is_set():
            cmd = input().strip().lower()
            if cmd == "settings":
                open_settings(cfg, dispatcher)
            elif cmd == "quit":
                should_stop.set()
            elif cmd == "help":
                print("Commands: settings | quit | help")
            else:
                print("Unknown command. Type help.")
    threading.Thread(target=console_commands, daemon=True).start()

    audio.start()

    partial_buffer = ""
    listening_for_command = False
    capture_text = ""
    last_trigger_time = 0
    COMMAND_WINDOW_SEC = 5

    try:
        while not should_stop.is_set():
            data = audio.read()
            fragment = transcriber.accept_audio(data)
            if fragment:
                fragment_lower = fragment.lower().strip()
                # Detect trigger
                if not listening_for_command and TRIGGER_WORD in fragment_lower.split():
                    listening_for_command = True
                    capture_text = ""
                    last_trigger_time = time.time()
                    logger.info("Trigger detected")
                    speaker("Yes?")
                elif listening_for_command:
                    # accumulate
                    capture_text += " " + fragment_lower
                    # If silence or time window exceeded, dispatch
                    if time.time() - last_trigger_time > COMMAND_WINDOW_SEC:
                        spoken = capture_text.strip()
                        if spoken:
                            logger.info(f"Captured command: {spoken}")
                            dispatcher.handle(spoken)
                        listening_for_command = False
                        capture_text = ""
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        should_stop.set()
        audio.stop()
        speaker("Mikey shutting down.")

if __name__ == "__main__":
    main()