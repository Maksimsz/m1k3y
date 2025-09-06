import os
import platform
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_time():
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

def shutdown_system():
    system = platform.system().lower()
    if system == "windows":
        cmd = ["shutdown", "/s", "/t", "5"]
    elif system == "darwin":
        cmd = ["osascript", "-e", 'tell app "System Events" to shut down']
    else:
        cmd = ["shutdown", "-h", "now"]
    subprocess.Popen(cmd)
    return "System shutdown initiated."

def open_app(target: Optional[str]):
    if not target:
        return "No application specified."
    system = platform.system().lower()
    if system == "windows":
        subprocess.Popen(["start", "", target], shell=True)
    elif system == "darwin":
        subprocess.Popen(["open", "-a", target])
    else:
        subprocess.Popen([target])
    return f"Attempted to open {target}."

def list_dir(path: Optional[str] = None):
    p = path or os.getcwd()
    try:
        return ", ".join(os.listdir(p)[:30])
    except Exception as e:
        return f"Error: {e}"