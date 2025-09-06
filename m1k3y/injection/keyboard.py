import time
from pynput.keyboard import Controller

_keyboard = Controller()

def type_text(text: str, delay=0.005):
    for ch in text:
        _keyboard.type(ch)
        time.sleep(delay)