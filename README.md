# M1K3Y (Mikey) – Local AI Desktop Assistant

M1K3Y is a fully local AI assistant that:
- Listens for the trigger word "mikey"
- Transcribes speech offline using Vosk
- Uses a local Mistral model served by Ollama
- Executes actions with a risk/confirmation framework
- Can inject text into the active window
- Provides a settings UI to configure microphone, voice, and model

## Features
- Offline speech recognition
- Offline TTS
- Local LLM (no cloud calls)
- Risk classification of commands
- Confirmation dialog or voice confirmation
- Modular action registry
- Extensible parser

## Quick Start

### 1. Prerequisites
Install Python 3.11+ and Ollama. Pull model:
```bash
ollama pull mistral
```

### 2. Clone / Create Project
```bash
git clone <your-repo-url> m1k3y
cd m1k3y
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run
```bash
python -m m1k3y.main
```

### 4. Speak
Say: "mikey what’s the date today"

### 5. Settings Window
Press Ctrl+Shift+S in console or use system tray (future enhancement) to open settings.

## Configuration
A `user_config.json` file will be generated under `m1k3y/data/`. You can edit while stopped or via settings UI.

## Risk Levels
- LOW: print time, say hello
- MEDIUM: open application, type text
- HIGH: delete files, shutdown system (requires confirmation)

## Adding Actions
Add a function in `actions/system_actions.py` and register it in `actions/registry.py`.

## Limitations / Notes
- Simple keyword trigger (can upgrade to proper wake-word model later).
- Confirmation is heuristic-based, always review `risk.py`.
- Cross-platform file operations differ; adapt commands accordingly.

## Roadmap (Ideas)
- Tray icon integration
- Continuous conversation context window
- Hot-reload for action modules
- Enhanced semantic intent classification

## Security Warning
Even with confirmation, action execution can be dangerous. Use a strict allowlist and never run as admin/root.

## License
(Choose one)
