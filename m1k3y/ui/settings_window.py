import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from ..config import AppConfig, save_config

class SettingsWindow:
    def __init__(self, root, cfg: AppConfig, on_update):
        self.root = root
        self.cfg = cfg
        self.on_update = on_update
        self.build()

    def build(self):
        self.root.title("M1K3Y Settings")
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        # Mic devices
        devices = sd.query_devices()
        mic_indices = [i for i, d in enumerate(devices) if d["max_input_channels"] > 0]

        ttk.Label(frm, text="Microphone:").grid(row=0, column=0, sticky="w")
        self.mic_var = tk.StringVar(value=str(self.cfg.mic_device_index) if self.cfg.mic_device_index is not None else "")
        self.mic_combo = ttk.Combobox(frm, textvariable=self.mic_var, values=[str(i) for i in mic_indices])
        self.mic_combo.grid(row=0, column=1, sticky="ew")

        ttk.Label(frm, text="Model Name:").grid(row=1, column=0, sticky="w")
        self.model_var = tk.StringVar(value=self.cfg.model_name)
        ttk.Entry(frm, textvariable=self.model_var).grid(row=1, column=1, sticky="ew")

        self.enable_inject = tk.BooleanVar(value=self.cfg.enable_text_injection)
        ttk.Checkbutton(frm, text="Enable Text Injection", variable=self.enable_inject).grid(row=2, column=0, columnspan=2, sticky="w")

        def save_and_close():
            self.cfg.model_name = self.model_var.get().strip()
            val = self.mic_var.get().strip()
            self.cfg.mic_device_index = int(val) if val.isdigit() else None
            self.cfg.enable_text_injection = self.enable_inject.get()
            save_config(self.cfg)
            self.on_update(self.cfg)
            self.root.destroy()

        ttk.Button(frm, text="Save", command=save_and_close).grid(row=99, column=0, pady=10)
        ttk.Button(frm, text="Cancel", command=self.root.destroy).grid(row=99, column=1, pady=10)
        frm.columnconfigure(1, weight=1)